import os
import json as _json
import threading
import urllib.request
import urllib.parse
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.controllers import content as content_ctrl

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    # `about` is provided by the app context processor (cached there).
    # Cache heavier lists to reduce DB load under frequent pings.
    c = current_app.extensions.get('cache')

    projects = None
    projects_list = None
    if c:
        projects = c.get('projects')
        projects_list = c.get('projects_list')

    if projects is None:
        projects = content_ctrl.get_all_projects()
        if c:
            try:
                c.set('projects', projects, timeout=current_app.config.get('CACHE_DEFAULT_TIMEOUT', 300))
            except Exception:
                pass

    if projects_list is None:
        projects_list = []
        for p in projects:
            projects_list.append({
                "id": p.id,
                "title": p.title,
                "tagline": p.tagline,
                "desc": p.description,
                "tech": p.tech_stack or "",
                "image": p.image_url or "",
                "github": p.github_url or "",
                "demo": p.demo_url or "",
                "featured": bool(p.is_featured),
            })
        if c:
            try:
                c.set('projects_list', projects_list, timeout=current_app.config.get('CACHE_DEFAULT_TIMEOUT', 300))
            except Exception:
                pass

    skills_by_category = content_ctrl.get_skills_by_category()
    experience = content_ctrl.get_all_experience()

    from app.models.content import BeyondCard
    beyond_cards = None
    if c:
        beyond_cards = c.get('beyond_cards')
    if beyond_cards is None:
        beyond_cards = BeyondCard.query.order_by(BeyondCard.order).all()
        if c:
            try:
                c.set('beyond_cards', beyond_cards, timeout=current_app.config.get('CACHE_DEFAULT_TIMEOUT', 300))
            except Exception:
                pass

    return render_template(
        "index.html",
        projects=projects,
        projects_list=projects_list,
        skills_by_category=skills_by_category,
        experience=experience,
        beyond_cards=beyond_cards,
    )


@public_bp.route("/about")
def about():
    skills_by_category = content_ctrl.get_skills_by_category()
    return render_template(
        "about.html",
        skills_by_category=skills_by_category,
    )


@public_bp.route('/healthz')
def healthz():
    # Lightweight health endpoint that does not touch the database.
    return ('OK', 200)


@public_bp.route("/projects")
def projects():
    # Redirect to single-page index anchor so old routes still work
    return redirect(url_for('public.index') + '#projects')


@public_bp.route("/experience")
def experience():
    return redirect(url_for('public.index') + '#experience')


@public_bp.route("/beyond")
def beyond():
    return redirect(url_for('public.index') + '#beyond')


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    recaptcha_site_key = os.environ.get("RECAPTCHA_SITE_KEY", "")

    # For GET requests, redirect to the single-page contact section
    if request.method == "GET":
        return redirect(url_for('public.index') + '#contact')

    # ── Bot checks ────────────────────────────────────────────
    # 1. Honeypot
    if request.form.get("website", "").strip():
        flash("Message sent! I'll get back to you soon.", "success")
        return redirect(url_for("public.contact"))

    # 2. Timing
    try:
        import time
        form_time = int(request.form.get("_t", "0"))
        elapsed = (int(time.time() * 1000) - form_time) / 1000
        if elapsed < 3:
            flash("Message sent! I'll get back to you soon.", "success")
            return redirect(url_for("public.contact"))
    except (ValueError, TypeError):
        pass

    # 3. reCAPTCHA server-side verification
    recaptcha_secret = os.environ.get("RECAPTCHA_SECRET_KEY", "")
    if recaptcha_secret:
        try:
            token = request.form.get("g-recaptcha-response", "")
            data = urllib.parse.urlencode({"secret": recaptcha_secret, "response": token}).encode()
            req = urllib.request.Request("https://www.google.com/recaptcha/api/siteverify", data=data)
            resp = _json.loads(urllib.request.urlopen(req, timeout=5).read())
            if not resp.get("success"):
                flash("Please complete the reCAPTCHA.", "error")
                return redirect(url_for("public.contact"))
        except Exception:
            pass  # Let through if reCAPTCHA check fails due to network

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("public.contact"))

    try:
        content_ctrl.save_contact_message(
            {"name": name, "email": email, "subject": subject, "message": message}
        )
    except Exception as exc:
        flash("Something went wrong saving your message. Please try again.", "error")
        return redirect(url_for("public.contact"))

    # Send email notification via Resend in a background thread
    def _send_email():
        try:
            resend_key = os.environ.get("RESEND_API_KEY")
            if not resend_key:
                return
            payload = _json.dumps({
                "from": "Portfolio Contact <onboarding@resend.dev>",
                "to": ["me@shantanumallik.com"],
                "subject": f"Portfolio contact: {subject or name}",
                "text": f"Name: {name}\nEmail: {email}\nSubject: {subject or '(none)'}\n\n{message}",
            }).encode()
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=payload,
                headers={"Authorization": f"Bearer {resend_key}", "Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    threading.Thread(target=_send_email, daemon=True).start()

    flash("Message sent! I'll get back to you soon.", "success")
    return redirect(url_for("public.contact"))
