from app.models.content import About, Skill, Project, Experience, ContactMessage
from app import db


def get_about():
    about = About.query.first()
    if not about:
        about = About()
        db.session.add(about)
        db.session.commit()
    return about


def update_about(about, data):
    about.hero_role = data.get("hero_role", about.hero_role)
    about.hero_tagline = data.get("hero_tagline", about.hero_tagline)
    about.hero_subtitle = data.get("hero_subtitle", about.hero_subtitle)
    about.bio = data.get("bio", about.bio)
    about.location = data.get("location", about.location)
    about.email = data.get("email", about.email)
    about.linkedin_url = data.get("linkedin_url", about.linkedin_url)
    about.github_url = data.get("github_url", about.github_url)
    about.resume_url = data.get("resume_url", about.resume_url)
    db.session.commit()


def get_skills_by_category():
    skills = Skill.query.order_by(Skill.category, Skill.order).all()
    grouped = {}
    for skill in skills:
        grouped.setdefault(skill.category, []).append(skill)
    return grouped


def get_featured_skills():
    return Skill.query.filter_by(is_featured=True).order_by(Skill.order).all()


def get_all_skills():
    return Skill.query.order_by(Skill.category, Skill.order).all()


def add_skill(data):
    skill = Skill(
        name=data["name"],
        category=data["category"],
        proficiency=int(data.get("proficiency", 90)),
        icon=data.get("icon", "code"),
        order=int(data.get("order", 0)),
        is_featured=data.get("is_featured") == "on",
    )
    db.session.add(skill)
    db.session.commit()
    return skill


def update_skill(skill, data):
    skill.name = data.get("name", skill.name)
    skill.category = data.get("category", skill.category)
    skill.proficiency = int(data.get("proficiency", skill.proficiency))
    skill.icon = data.get("icon", skill.icon)
    skill.order = int(data.get("order", skill.order))
    skill.is_featured = data.get("is_featured") == "on"
    db.session.commit()


def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()


def get_featured_projects():
    return Project.query.filter_by(is_featured=True).order_by(Project.order).all()


def get_all_projects():
    return Project.query.order_by(Project.order).all()


def add_project(data):
    project = Project(
        title=data["title"],
        tagline=data.get("tagline", ""),
        description=data["description"],
        tech_stack=data.get("tech_stack", ""),
        github_url=data.get("github_url", ""),
        demo_url=data.get("demo_url", ""),
        image_url=data.get("image_url", ""),
        is_featured=data.get("is_featured") == "on",
        order=int(data.get("order", 0)),
    )
    db.session.add(project)
    db.session.commit()
    return project


def update_project(project, data):
    project.title = data.get("title", project.title)
    project.tagline = data.get("tagline", project.tagline)
    project.description = data.get("description", project.description)
    project.tech_stack = data.get("tech_stack", project.tech_stack)
    project.github_url = data.get("github_url", project.github_url)
    project.demo_url = data.get("demo_url", project.demo_url)
    project.image_url = data.get("image_url", project.image_url)
    project.is_featured = data.get("is_featured") == "on"
    project.order = int(data.get("order", project.order))
    db.session.commit()


def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()


def get_all_experience():
    return Experience.query.order_by(Experience.order).all()


def add_experience(data):
    exp = Experience(
        company=data["company"],
        role=data["role"],
        start_date=data["start_date"],
        end_date=data.get("end_date", "Present"),
        description=data["description"],
        technologies=data.get("technologies", ""),
        order=int(data.get("order", 0)),
    )
    db.session.add(exp)
    db.session.commit()
    return exp


def update_experience(exp, data):
    exp.company = data.get("company", exp.company)
    exp.role = data.get("role", exp.role)
    exp.start_date = data.get("start_date", exp.start_date)
    exp.end_date = data.get("end_date", exp.end_date)
    exp.description = data.get("description", exp.description)
    exp.technologies = data.get("technologies", exp.technologies)
    exp.order = int(data.get("order", exp.order))
    db.session.commit()


def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()


def save_contact_message(data):
    msg = ContactMessage(
        name=data["name"],
        email=data["email"],
        subject=data.get("subject", ""),
        message=data["message"],
    )
    db.session.add(msg)
    db.session.commit()
    return msg


def get_all_messages():
    return ContactMessage.query.order_by(ContactMessage.received_at.desc()).all()


def mark_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()


def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
