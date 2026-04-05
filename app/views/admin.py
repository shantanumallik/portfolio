from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.controllers import auth as auth_ctrl
from app.controllers import content as content_ctrl
from app.models.content import Skill, Project, Experience, BeyondCard

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if auth_ctrl.authenticate(username, password):
            flash("Welcome back!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin.dashboard"))
        flash("Invalid credentials. Please try again.", "error")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    auth_ctrl.logout()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@login_required
def dashboard():
    from app.models.content import Project, Skill, Experience, ContactMessage
    stats = {
        "projects": Project.query.count(),
        "skills": Skill.query.count(),
        "experience": Experience.query.count(),
        "messages": ContactMessage.query.count(),
        "unread": ContactMessage.query.filter_by(is_read=False).count(),
    }
    messages = content_ctrl.get_all_messages()
    return render_template("admin/dashboard.html", stats=stats, messages=messages)


# ── About ─────────────────────────────────────────────────────────────────────

@admin_bp.route("/about", methods=["GET", "POST"])
@login_required
def about():
    about = content_ctrl.get_about()
    if request.method == "POST":
        content_ctrl.update_about(about, request.form)
        flash("About section updated.", "success")
        return redirect(url_for("admin.about"))
    return render_template("admin/about.html", about=about)


# ── Skills ────────────────────────────────────────────────────────────────────

@admin_bp.route("/skills")
@login_required
def skills():
    all_skills = content_ctrl.get_all_skills()
    return render_template("admin/skills.html", skills=all_skills)


@admin_bp.route("/skills/add", methods=["POST"])
@login_required
def skill_add():
    content_ctrl.add_skill(request.form)
    flash("Skill added.", "success")
    return redirect(url_for("admin.skills"))


@admin_bp.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
@login_required
def skill_edit(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == "POST":
        content_ctrl.update_skill(skill, request.form)
        flash("Skill updated.", "success")
        return redirect(url_for("admin.skills"))
    return render_template("admin/skill_edit.html", skill=skill)


@admin_bp.route("/skills/<int:skill_id>/delete", methods=["POST"])
@login_required
def skill_delete(skill_id):
    content_ctrl.delete_skill(skill_id)
    flash("Skill deleted.", "success")
    return redirect(url_for("admin.skills"))


# ── Projects ──────────────────────────────────────────────────────────────────

@admin_bp.route("/projects")
@login_required
def projects():
    all_projects = content_ctrl.get_all_projects()
    return render_template("admin/projects.html", projects=all_projects)


@admin_bp.route("/projects/add", methods=["POST"])
@login_required
def project_add():
    content_ctrl.add_project(request.form)
    flash("Project added.", "success")
    return redirect(url_for("admin.projects"))


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == "POST":
        content_ctrl.update_project(project, request.form)
        flash("Project updated.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_edit.html", project=project)


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def project_delete(project_id):
    content_ctrl.delete_project(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for("admin.projects"))


# ── Experience ────────────────────────────────────────────────────────────────

@admin_bp.route("/experience")
@login_required
def experience():
    all_exp = content_ctrl.get_all_experience()
    return render_template("admin/experience.html", experience=all_exp)


@admin_bp.route("/experience/add", methods=["POST"])
@login_required
def experience_add():
    content_ctrl.add_experience(request.form)
    flash("Experience entry added.", "success")
    return redirect(url_for("admin.experience"))


@admin_bp.route("/experience/<int:exp_id>/edit", methods=["GET", "POST"])
@login_required
def experience_edit(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    if request.method == "POST":
        content_ctrl.update_experience(exp, request.form)
        flash("Experience updated.", "success")
        return redirect(url_for("admin.experience"))
    return render_template("admin/experience_edit.html", exp=exp)


@admin_bp.route("/experience/<int:exp_id>/delete", methods=["POST"])
@login_required
def experience_delete(exp_id):
    content_ctrl.delete_experience(exp_id)
    flash("Experience entry deleted.", "success")
    return redirect(url_for("admin.experience"))


# ── Messages ──────────────────────────────────────────────────────────────────

@admin_bp.route("/messages/<int:msg_id>/read", methods=["POST"])
@login_required
def message_read(msg_id):
    content_ctrl.mark_message_read(msg_id)
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/messages/<int:msg_id>/delete", methods=["POST"])
@login_required
def message_delete(msg_id):
    content_ctrl.delete_message(msg_id)
    flash("Message deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── Password Change ───────────────────────────────────────────────────────────

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        current_pw = request.form.get("current_password", "")
        new_pw = request.form.get("new_password", "")
        confirm_pw = request.form.get("confirm_password", "")
        if new_pw != confirm_pw:
            flash("New passwords do not match.", "error")
        elif not auth_ctrl.change_password(current_user, current_pw, new_pw):
            flash("Current password is incorrect.", "error")
        else:
            flash("Password changed successfully.", "success")
    return render_template("admin/settings.html")


# ── Inline Edit JSON API ───────────────────────────────────────────────────────

def _about_dict(a):
    return {
        "hero_tagline": a.hero_tagline or "",
        "hero_subtitle": a.hero_subtitle or "",
        "bio": a.bio or "",
        "location": a.location or "",
        "email": a.email or "",
        "linkedin_url": a.linkedin_url or "",
        "github_url": a.github_url or "",
        "resume_url": a.resume_url or "",
    }


def _exp_dict(e):
    return {
        "id": e.id,
        "company": e.company,
        "role": e.role,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "description": e.description,
        "technologies": e.technologies or "",
        "order": e.order,
    }


def _project_dict(p):
    return {
        "id": p.id,
        "title": p.title,
        "tagline": p.tagline or "",
        "description": p.description,
        "tech_stack": p.tech_stack or "",
        "github_url": p.github_url or "",
        "demo_url": p.demo_url or "",
        "image_url": p.image_url or "",
        "is_featured": p.is_featured,
        "order": p.order,
    }


def _skill_dict(s):
    return {
        "id": s.id,
        "name": s.name,
        "category": s.category,
        "proficiency": s.proficiency,
        "is_featured": s.is_featured,
        "order": s.order,
    }


def _bool_to_form(data, field="is_featured"):
    """Convert JSON bool to form-style 'on'/'' for existing controllers."""
    if field in data:
        data[field] = "on" if data[field] else ""
    return data


@admin_bp.route("/api/about", methods=["GET", "PUT"])
@login_required
def api_about():
    about = content_ctrl.get_about()
    if request.method == "PUT":
        content_ctrl.update_about(about, request.get_json(force=True) or {})
        return jsonify({"ok": True, "data": _about_dict(about)})
    return jsonify(_about_dict(about))


@admin_bp.route("/api/experience", methods=["POST"])
@login_required
def api_experience_add():
    exp = content_ctrl.add_experience(request.get_json(force=True) or {})
    return jsonify({"ok": True, "data": _exp_dict(exp)}), 201


@admin_bp.route("/api/experience/<int:exp_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_experience_item(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    if request.method == "DELETE":
        content_ctrl.delete_experience(exp_id)
        return jsonify({"ok": True})
    if request.method == "PUT":
        content_ctrl.update_experience(exp, request.get_json(force=True) or {})
        return jsonify({"ok": True, "data": _exp_dict(exp)})
    return jsonify(_exp_dict(exp))


@admin_bp.route("/api/projects", methods=["POST"])
@login_required
def api_project_add():
    data = _bool_to_form(request.get_json(force=True) or {})
    project = content_ctrl.add_project(data)
    return jsonify({"ok": True, "data": _project_dict(project)}), 201


@admin_bp.route("/api/projects/<int:project_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_project_item(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == "DELETE":
        content_ctrl.delete_project(project_id)
        return jsonify({"ok": True})
    if request.method == "PUT":
        data = _bool_to_form(request.get_json(force=True) or {})
        content_ctrl.update_project(project, data)
        return jsonify({"ok": True, "data": _project_dict(project)})
    return jsonify(_project_dict(project))


@admin_bp.route("/api/skills", methods=["POST"])
@login_required
def api_skill_add():
    data = _bool_to_form(request.get_json(force=True) or {})
    skill = content_ctrl.add_skill(data)
    return jsonify({"ok": True, "data": _skill_dict(skill)}), 201


@admin_bp.route("/api/skills/<int:skill_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_skill_item(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == "DELETE":
        content_ctrl.delete_skill(skill_id)
        return jsonify({"ok": True})
    if request.method == "PUT":
        data = _bool_to_form(request.get_json(force=True) or {})
        content_ctrl.update_skill(skill, data)
        return jsonify({"ok": True, "data": _skill_dict(skill)})
    return jsonify(_skill_dict(skill))


# ── Beyond Cards ──────────────────────────────────────────────────────────────

@admin_bp.route("/beyond")
@login_required
def beyond():
    cards = BeyondCard.query.order_by(BeyondCard.order).all()
    return render_template("admin/beyond.html", cards=cards)


@admin_bp.route("/beyond/add", methods=["POST"])
@login_required
def beyond_add():
    from app import db
    card = BeyondCard(
        icon=request.form.get("icon", "🌍").strip(),
        title=request.form.get("title", "").strip(),
        description=request.form.get("description", "").strip(),
        order=int(request.form.get("order", 0)),
    )
    db.session.add(card)
    db.session.commit()
    flash("Card added.", "success")
    return redirect(url_for("admin.beyond"))


@admin_bp.route("/beyond/<int:card_id>/edit", methods=["GET", "POST"])
@login_required
def beyond_edit(card_id):
    from app import db
    card = BeyondCard.query.get_or_404(card_id)
    if request.method == "POST":
        card.icon = request.form.get("icon", card.icon).strip()
        card.title = request.form.get("title", card.title).strip()
        card.description = request.form.get("description", card.description).strip()
        card.order = int(request.form.get("order", card.order))
        db.session.commit()
        flash("Card updated.", "success")
        return redirect(url_for("admin.beyond"))
    return render_template("admin/beyond_edit.html", card=card)


@admin_bp.route("/beyond/<int:card_id>/delete", methods=["POST"])
@login_required
def beyond_delete(card_id):
    from app import db
    card = BeyondCard.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    flash("Card deleted.", "success")
    return redirect(url_for("admin.beyond"))


# ── Beyond Cards JSON API ──────────────────────────────────────────────────────

def _beyond_dict(c):
    return {"id": c.id, "icon": c.icon, "title": c.title, "description": c.description, "order": c.order}


@admin_bp.route("/api/beyond", methods=["POST"])
@login_required
def api_beyond_add():
    from app import db
    data = request.get_json(force=True) or {}
    cards = BeyondCard.query.order_by(BeyondCard.order).all()
    next_order = (cards[-1].order + 10) if cards else 10
    card = BeyondCard(
        icon=data.get("icon", "🌍").strip(),
        title=data.get("title", "").strip(),
        description=data.get("description", "").strip(),
        order=int(data.get("order", next_order)),
    )
    db.session.add(card)
    db.session.commit()
    return jsonify({"ok": True, "data": _beyond_dict(card)}), 201


@admin_bp.route("/api/beyond/<int:card_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_beyond_item(card_id):
    from app import db
    card = BeyondCard.query.get_or_404(card_id)
    if request.method == "DELETE":
        db.session.delete(card)
        db.session.commit()
        return jsonify({"ok": True})
    if request.method == "PUT":
        data = request.get_json(force=True) or {}
        card.icon = data.get("icon", card.icon).strip()
        card.title = data.get("title", card.title).strip()
        card.description = data.get("description", card.description).strip()
        db.session.commit()
        return jsonify({"ok": True, "data": _beyond_dict(card)})
    return jsonify(_beyond_dict(card))


@admin_bp.route("/api/beyond/reorder", methods=["POST"])
@login_required
def api_beyond_reorder():
    from app import db
    ids = (request.get_json(force=True) or {}).get("ids", [])
    for i, card_id in enumerate(ids):
        card = BeyondCard.query.get(card_id)
        if card:
            card.order = (i + 1) * 10
    db.session.commit()
    return jsonify({"ok": True})
