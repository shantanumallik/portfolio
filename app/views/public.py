import os
import random
import smtplib
import threading
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.controllers import content as content_ctrl

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    about = content_ctrl.get_about()
    return render_template("index.html", about=about)


@public_bp.route("/about")
def about():
    skills_by_category = content_ctrl.get_skills_by_category()
    return render_template(
        "about.html",
        skills_by_category=skills_by_category,
    )


@public_bp.route("/projects")
def projects():
    projects = content_ctrl.get_all_projects()
    return render_template("projects.html", projects=projects)


@public_bp.route("/experience")
def experience():
    experience = content_ctrl.get_all_experience()
    return render_template("experience.html", experience=experience)


@public_bp.route("/beyond")
def beyond():
    from app.models.content import BeyondCard
    cards = BeyondCard.query.order_by(BeyondCard.order).all()
    return render_template("beyond.html", cards=cards)


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        # Generate math captcha
        a, b = random.randint(2, 9), random.randint(1, 9)
        session["captcha_answer"] = a + b
        session["captcha_q"] = f"{a} + {b}"
        return render_template("contact.html", captcha_q=session["captcha_q"])

    # ── Bot checks ────────────────────────────────────────────
    # 1. Honeypot
    if request.form.get("website", "").strip():
        flash("Message sent! I'll get back to you soon.", "success")
        return redirect(url_for("public.contact"))

    # 2. Timing
    try:
        form_time = int(request.form.get("_t", "0"))
        import time
        elapsed = (int(time.time() * 1000) - form_time) / 1000
        if elapsed < 3:
            flash("Message sent! I'll get back to you soon.", "success")
            return redirect(url_for("public.contact"))
    except (ValueError, TypeError):
        pass

    # 3. Math captcha
    expected = session.pop("captcha_answer", None)
    try:
        given = int(request.form.get("captcha_answer", ""))
        if expected is None or given != expected:
            flash("Captcha answer incorrect. Please try again.", "error")
            return redirect(url_for("public.contact"))
    except (ValueError, TypeError):
        flash("Captcha answer incorrect. Please try again.", "error")
        return redirect(url_for("public.contact"))

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

    # Send email notification in background thread so SMTP never blocks the response
    def _send_email():
        try:
            mail_user = os.environ.get("MAIL_USER")
            mail_pass = os.environ.get("MAIL_PASSWORD")
            if not mail_user or not mail_pass:
                return
            body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject or '(none)'}\n\n"
                f"{message}"
            )
            msg = MIMEText(body)
            msg["Subject"] = f"Portfolio contact: {subject or name}"
            msg["From"] = mail_user
            msg["To"] = "me@shantanumallik.com"
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                server.starttls()
                server.login(mail_user, mail_pass)
                server.sendmail(mail_user, "me@shantanumallik.com", msg.as_string())
        except Exception:
            pass

    threading.Thread(target=_send_email, daemon=True).start()

    flash("Message sent! I'll get back to you soon.", "success")
    return redirect(url_for("public.contact"))
