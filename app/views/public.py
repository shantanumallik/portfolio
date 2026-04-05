import os
import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, flash, redirect, url_for
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


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("public.contact"))

    content_ctrl.save_contact_message(
        {"name": name, "email": email, "subject": subject, "message": message}
    )

    # Email notification
    try:
        mail_user = os.environ.get("MAIL_USER")
        mail_pass = os.environ.get("MAIL_PASSWORD")
        if mail_user and mail_pass:
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
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(mail_user, mail_pass)
                server.sendmail(mail_user, "me@shantanumallik.com", msg.as_string())
    except Exception:
        pass  # Don't break form submission if email fails

    flash("Message sent! I'll get back to you soon.", "success")
    return redirect(url_for("public.contact"))
