#!/usr/bin/env python3
"""
Initialise the database and create the first admin user.
Run once: python init_db.py
"""

import getpass
import sys
from app import create_app, db
from app.controllers.auth import create_admin
from app.models.content import About, Skill, Project, Experience


def seed_default_content():
    """Insert sample content so the portfolio isn't empty on first run."""

    # About
    if About.query.count() == 0:
        about = About(
            hero_tagline="Engineering Intelligence. Automating the Future.",
            hero_subtitle="SVT/PV Engineer at Ciena · Python · Agentic AI",
            bio=(
                "I'm an SVT/PV Engineer at Ciena with a passion for Python-based "
                "test automation and Agentic AI systems. I design and execute "
                "system verification and product validation frameworks that ensure "
                "network products ship with confidence — and increasingly, I build "
                "AI agents that make that process smarter and faster."
            ),
            location="Ottawa, Canada",
            email="",
            linkedin_url="",
            github_url="",
            resume_url="",
        )
        db.session.add(about)

    # Skills
    if Skill.query.count() == 0:
        skills_data = [
            ("Python",              "Language",  95, True,  0),
            ("Pytest",              "Language",  90, True,  1),
            ("Bash / Shell",        "Language",  70, False, 2),
            ("LangChain",           "Agentic AI",88, True,  0),
            ("LangGraph",           "Agentic AI",82, True,  1),
            ("OpenAI API",          "Agentic AI",85, False, 2),
            ("Prompt Engineering",  "Agentic AI",90, False, 3),
            ("RAG Pipelines",       "Agentic AI",80, False, 4),
            ("Test Automation",     "SVT / PV",  95, True,  0),
            ("CI/CD (Jenkins)",     "SVT / PV",  82, False, 1),
            ("NETCONF / YANG",      "SVT / PV",  75, False, 2),
            ("Network Protocols",   "SVT / PV",  78, False, 3),
            ("Git",                 "Tools",     88, False, 0),
            ("Docker",              "Tools",     72, False, 1),
            ("SQLAlchemy",          "Tools",     80, False, 2),
        ]
        for name, cat, prof, featured, order in skills_data:
            db.session.add(Skill(
                name=name, category=cat, proficiency=prof,
                is_featured=featured, order=order
            ))

    # Experience
    if Experience.query.count() == 0:
        db.session.add(Experience(
            company="Ciena",
            role="SVT/PV Engineer",
            start_date="Jan 2022",
            end_date="Present",
            description=(
                "Lead system verification and product validation for optical "
                "networking gear. Building Python automation frameworks and "
                "pioneering Agentic AI integration into the test lifecycle — "
                "reducing regression cycle time and improving defect detection "
                "across multiple product lines."
            ),
            technologies="Python, Pytest, LangChain, Jenkins, NETCONF, Git",
            order=0,
        ))

    # Projects
    if Project.query.count() == 0:
        projects_data = [
            (
                "Agentic Test Orchestrator",
                "AI-driven test generation & execution",
                (
                    "A multi-agent system using LangGraph that analyses system "
                    "specifications and automatically generates, prioritises, and "
                    "executes SVT test suites — cutting manual test authoring time "
                    "by 60%."
                ),
                "Python, LangGraph, Pytest, OpenAI API",
                True, 0,
            ),
            (
                "Network PV Automation Framework",
                "End-to-end product validation pipeline",
                (
                    "Modular Python framework for automated product validation of "
                    "optical networking equipment at Ciena, fully integrated with "
                    "CI/CD pipelines for continuous regression testing."
                ),
                "Python, Pytest, Jenkins, NETCONF, Docker",
                True, 1,
            ),
            (
                "RAG Knowledge Agent",
                "Retrieval-augmented assistant for internal docs",
                (
                    "Conversational agent that ingests technical documentation and "
                    "answers engineering questions in natural language using RAG, "
                    "vector search, and an OpenAI backbone."
                ),
                "Python, LangChain, Pinecone, FastAPI, OpenAI",
                False, 2,
            ),
        ]
        for title, tagline, desc, tech, featured, order in projects_data:
            db.session.add(Project(
                title=title, tagline=tagline, description=desc,
                tech_stack=tech, is_featured=featured, order=order,
            ))

    db.session.commit()
    print("✔  Default content seeded.")


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✔  Database tables created.")

        seed_default_content()

        from app.models.admin import AdminUser
        if AdminUser.query.count() == 0:
            print("\n── Create admin account ──────────────────────")
            username = input("Admin username [admin]: ").strip() or "admin"
            while True:
                password = getpass.getpass("Admin password (min 8 chars): ")
                if len(password) < 8:
                    print("  Password must be at least 8 characters.")
                    continue
                confirm = getpass.getpass("Confirm password: ")
                if password != confirm:
                    print("  Passwords do not match. Try again.")
                    continue
                break
            try:
                create_admin(username, password)
                print(f"✔  Admin user '{username}' created.")
            except ValueError as e:
                print(f"  Warning: {e}")
        else:
            print("✔  Admin user already exists — skipping creation.")

        print("\n🚀  Done! Run the app with:  python run.py")


if __name__ == "__main__":
    main()
