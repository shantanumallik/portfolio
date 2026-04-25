from app import db
from datetime import datetime


class About(db.Model):
    __tablename__ = "about"

    id = db.Column(db.Integer, primary_key=True)
    hero_role = db.Column(db.String(150), default="Software Systems Engineer & PV Engineer.")
    hero_tagline = db.Column(db.String(300), nullable=False, default="Engineering Intelligence. Automating the Future.")
    hero_subtitle = db.Column(db.String(200), nullable=False, default="SVT/PV Engineer at Ciena")
    bio = db.Column(db.Text, nullable=False, default="")
    location = db.Column(db.String(100), default="")
    email = db.Column(db.String(120), default="")
    linkedin_url = db.Column(db.String(255), default="")
    github_url = db.Column(db.String(255), default="")
    resume_url = db.Column(db.String(255), default="")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<About {self.id}>"


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g. "language", "framework", "tool", "domain"
    proficiency = db.Column(db.Integer, default=90)  # 0-100
    icon = db.Column(db.String(50), default="code")  # icon name/class
    order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Skill {self.name}>"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    tagline = db.Column(db.String(200), default="")
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(300), default="")  # comma-separated
    github_url = db.Column(db.String(255), default="")
    demo_url = db.Column(db.String(255), default="")
    image_url = db.Column(db.String(255), default="")
    is_featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    def __repr__(self):
        return f"<Project {self.title}>"


class Experience(db.Model):
    __tablename__ = "experience"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), default="Present")
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300), default="")
    order = db.Column(db.Integer, default=0)

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    def __repr__(self):
        return f"<Experience {self.company} - {self.role}>"


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage from {self.name}>"


class BeyondCard(db.Model):
    __tablename__ = "beyond_cards"

    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(10), default="🌍")
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<BeyondCard {self.title}>"
