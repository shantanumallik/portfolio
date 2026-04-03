from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.controllers import content as content_ctrl

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    about = content_ctrl.get_about()
    skills_by_category = content_ctrl.get_skills_by_category()
    featured_skills = content_ctrl.get_featured_skills()
    projects = content_ctrl.get_all_projects()
    experience = content_ctrl.get_all_experience()
    return render_template(
        "index.html",
        about=about,
        skills_by_category=skills_by_category,
        featured_skills=featured_skills,
        projects=projects,
        experience=experience,
    )


@public_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("public.index") + "#contact")

    content_ctrl.save_contact_message(
        {"name": name, "email": email, "subject": subject, "message": message}
    )
    flash("Message sent! I'll get back to you soon.", "success")
    return redirect(url_for("public.index") + "#contact")
