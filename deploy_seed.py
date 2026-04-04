"""
Runs on every Render deploy (build step).
Idempotent — only seeds if tables are empty.
Reads ADMIN_USERNAME / ADMIN_PASSWORD from environment for first-time admin creation.
"""
import os
from app import create_app, db
from app.models.content import About, Skill, Project, Experience
from app.models.admin import AdminUser
from app.controllers.auth import create_admin

app = create_app()

with app.app_context():
    db.create_all()

    # ── ABOUT ──────────────────────────────────────────────────────────────────
    about = About.query.first()
    if not about:
        about = About()
        db.session.add(about)

    about.hero_tagline  = "Software Systems Engineer at Ciena — building automation platforms and agentic AI systems for distributed networking infrastructure."
    about.hero_subtitle = "Python · Agentic AI · Distributed Systems · Backend Engineering"
    about.bio = (
        "Software Systems Engineer at Ciena, designing and shipping the internal platform that validates "
        "distributed optical networking hardware at 1.6 Tbps scale. My work spans Python backend services, "
        "REST APIs integrated into Jenkins CI/CD pipelines, and agentic AI workflows built with LangChain "
        "and LangGraph — systems that replace manual engineering effort with structured, machine-driven "
        "reasoning. Previously a Research Engineer at IIIT Delhi's Complex Systems Laboratory, and four "
        "years as a freelance backend developer shipping production systems to 50,000+ users."
    )
    about.location     = "Gurugram, Haryana, India"
    about.email        = "me@shantanumallik.com"
    about.linkedin_url = "https://www.linkedin.com/in/shantanumallik"
    about.github_url   = ""
    about.resume_url   = ""

    # ── SKILLS ─────────────────────────────────────────────────────────────────
    if Skill.query.count() == 0:
        skills = [
            # (name, category, proficiency, is_featured, order)
            ("Python",                  "Backend Engineering", 97, True,  0),
            ("REST API Design",         "Backend Engineering", 93, True,  1),
            ("Flask / FastAPI",         "Backend Engineering", 88, True,  2),
            ("PostgreSQL",              "Backend Engineering", 82, False, 3),
            ("Docker",                  "Backend Engineering", 80, False, 4),
            ("Linux",                   "Backend Engineering", 87, False, 5),

            ("Agentic AI Systems",      "Agentic AI",          93, True,  0),
            ("LangChain / LangGraph",   "Agentic AI",          89, True,  1),
            ("LLM Integration",         "Agentic AI",          87, True,  2),
            ("AI Failure Triaging",     "Agentic AI",          90, True,  3),
            ("RAG Pipelines",           "Agentic AI",          84, False, 4),
            ("Prompt Engineering",      "Agentic AI",          88, False, 5),

            ("Automation",              "Platform & CI/CD",    93, True,  0),
            ("Jenkins CI/CD",           "Platform & CI/CD",    90, True,  1),
            ("Distributed Systems",     "Platform & CI/CD",    84, True,  2),
            ("Grafana",                 "Platform & CI/CD",    80, False, 3),
            ("TestRail",                "Platform & CI/CD",    78, False, 4),

            ("Data Modeling",           "Data Engineering",    85, False, 0),
            ("Data Pipeline Design",    "Data Engineering",    83, False, 1),
            ("Large-Scale Data Analysis","Data Engineering",   80, False, 2),

            ("Git / GitHub",            "Tooling & Cloud",     92, False, 0),
            ("GCP",                     "Tooling & Cloud",     74, False, 1),
            ("Ruby on Rails",           "Tooling & Cloud",     70, False, 2),
            ("Heroku",                  "Tooling & Cloud",     72, False, 3),
        ]
        for name, cat, prof, featured, order in skills:
            db.session.add(Skill(
                name=name, category=cat, proficiency=prof,
                is_featured=featured, order=order
            ))

    # ── EXPERIENCE ─────────────────────────────────────────────────────────────
    if Experience.query.count() == 0:
        experience = [
            (
                "Ciena", "Software Systems Engineer", "Jan 2025", "Present",
                (
                    "Building the internal platform that validates distributed networking hardware "
                    "operating at up to 1.6 Tbps. Design and ship Python-based backend services and "
                    "REST APIs consumed by Jenkins CI/CD pipelines — automating firmware and system-build "
                    "validation across multiple hardware variants and reducing manual testing effort by 40–50%. "
                    "Developed an agentic failure triaging system using LangChain and LangGraph that ingests "
                    "raw test failures, clusters root causes via LLM reasoning chains, and delivers structured "
                    "debugging summaries — compressing triage time from hours to minutes. Architected Grafana "
                    "dashboards surfacing build-execution trends, test stability signals, and platform health "
                    "KPIs for engineering leadership."
                ),
                "Python, LangChain, LangGraph, REST APIs, Jenkins, Grafana, TestRail, CI/CD, Git, Linux",
                0,
            ),
            (
                "Complex Systems Laboratory / Foodoscope", "Research Intern", "Jan 2024", "Jan 2025",
                (
                    "Research Engineer at IIIT Delhi's Complex Systems Laboratory, building backend systems "
                    "and data APIs for large-scale food, nutrition, and health knowledge bases. "
                    "FlavorDB: data models and retrieval APIs for 934 natural ingredients and their "
                    "flavour-molecule compositions. RecipeDB: data pipelines and querying layer for "
                    "118,000+ recipes spanning 26 global regions. DietRx: a backend system linking "
                    "dietary ingredients to peer-reviewed therapeutic evidence."
                ),
                "Python, REST APIs, Data Modeling, Data Pipeline Design, PostgreSQL",
                1,
            ),
            (
                "Freelance", "Software Engineer", "Apr 2019", "Apr 2023",
                (
                    "Four years of end-to-end backend engineering delivery across startup and enterprise "
                    "engagements. Designed and shipped production-grade Python and Ruby on Rails systems "
                    "serving 50,000+ active users. Built automation-focused APIs that eliminated approximately "
                    "95% of clients' manual processing workloads. Managed full deployment pipelines on GCP "
                    "and Heroku, from schema design through production release."
                ),
                "Python, Flask, Ruby on Rails, REST APIs, PostgreSQL, Git, Linux, GCP, Heroku, CI/CD",
                2,
            ),
        ]
        for company, role, start, end, desc, tech, order in experience:
            db.session.add(Experience(
                company=company, role=role,
                start_date=start, end_date=end,
                description=desc, technologies=tech, order=order
            ))
    else:
        # Update existing experience descriptions
        updates = {
            1: (
                "Building the internal platform that validates distributed networking hardware "
                "operating at up to 1.6 Tbps. Design and ship Python-based backend services and "
                "REST APIs consumed by Jenkins CI/CD pipelines — automating firmware and system-build "
                "validation across multiple hardware variants and reducing manual testing effort by 40–50%. "
                "Developed an agentic failure triaging system using LangChain and LangGraph that ingests "
                "raw test failures, clusters root causes via LLM reasoning chains, and delivers structured "
                "debugging summaries — compressing triage time from hours to minutes. Architected Grafana "
                "dashboards surfacing build-execution trends, test stability signals, and platform health "
                "KPIs for engineering leadership."
            ),
            2: (
                "Research Engineer at IIIT Delhi's Complex Systems Laboratory, building backend systems "
                "and data APIs for large-scale food, nutrition, and health knowledge bases. "
                "FlavorDB: data models and retrieval APIs for 934 natural ingredients and their "
                "flavour-molecule compositions. RecipeDB: data pipelines and querying layer for "
                "118,000+ recipes spanning 26 global regions. DietRx: a backend system linking "
                "dietary ingredients to peer-reviewed therapeutic evidence."
            ),
            3: (
                "Four years of end-to-end backend engineering delivery across startup and enterprise "
                "engagements. Designed and shipped production-grade Python and Ruby on Rails systems "
                "serving 50,000+ active users. Built automation-focused APIs that eliminated approximately "
                "95% of clients' manual processing workloads. Managed full deployment pipelines on GCP "
                "and Heroku, from schema design through production release."
            ),
        }
        for exp_id, desc in updates.items():
            exp = db.session.get(Experience, exp_id)
            if exp:
                exp.description = desc

    # ── PROJECTS ───────────────────────────────────────────────────────────────
    if Project.query.count() == 0:
        projects = [
            (
                "Agentic Failure Triage System",
                "LLM-powered root-cause analysis for CI/CD test failures at scale",
                (
                    "Built at Ciena to address a core challenge in large-scale hardware validation: "
                    "extracting signal from thousands of test failures per build cycle. An agentic workflow "
                    "ingests structured failure logs from Jenkins CI/CD runs, uses LangGraph to orchestrate "
                    "multi-step LLM reasoning chains, and produces clustered root-cause summaries with "
                    "confidence scores and suggested remediation paths — compressing engineer triage time "
                    "from hours to minutes."
                ),
                "Python, LangChain, LangGraph, OpenAI, Jenkins, REST APIs, Git",
                "", "", "", True, 0,
            ),
            (
                "Internal Validation Platform",
                "Backend platform orchestrating 1.6 Tbps distributed systems testing",
                (
                    "Core backend contributor to Ciena's internal developer platform — a Python service "
                    "layer that orchestrates automated firmware and system-build validation across "
                    "distributed networking hardware at up to 1.6 Tbps. "
                    "Exposes REST APIs consumed by Jenkins CI/CD pipelines to trigger, monitor, and "
                    "report on thousands of test runs across hardware variants."
                ),
                "Python, REST APIs, Jenkins, Grafana, TestRail, CI/CD, Linux",
                "", "", "", True, 1,
            ),
            (
                "FlavorDB & RecipeDB APIs",
                "Data APIs powering 118k+ recipes and 934-ingredient flavour knowledge base",
                (
                    "At the Complex Systems Laboratory (IIIT Delhi), built the backend data services "
                    "underpinning two large-scale research knowledge bases. "
                    "RecipeDB: queryable API over 118,000+ recipes across 26 global regions. "
                    "FlavorDB: data models and retrieval APIs for 934 natural ingredients and their "
                    "flavour molecule profiles — used by food scientists globally."
                ),
                "Python, REST APIs, Data Modeling, Data Pipeline Design, PostgreSQL",
                "", "", "", False, 2,
            ),
            (
                "Freelance Backend Systems",
                "Production APIs and platforms scaled to 50,000+ users",
                (
                    "Four years of independent backend engineering across startup and enterprise engagements. "
                    "Built automation-first APIs eliminating ~95% of clients' manual processing workloads. "
                    "Delivered complete Python + Flask backends from schema design through cloud deployment, "
                    "serving 50,000+ active users in production."
                ),
                "Python, Flask, Ruby on Rails, REST APIs, PostgreSQL, GCP, Heroku, CI/CD",
                "", "", "", False, 3,
            ),
        ]
        for title, tagline, desc, tech, github, demo, image, featured, order in projects:
            db.session.add(Project(
                title=title, tagline=tagline, description=desc,
                tech_stack=tech, github_url=github, demo_url=demo,
                image_url=image, is_featured=featured, order=order
            ))
    else:
        # Update existing project descriptions and taglines
        proj_updates = {
            1: ("LLM-powered root-cause analysis for CI/CD test failures at scale",
                "Built at Ciena to address a core challenge in large-scale hardware validation: "
                "extracting signal from thousands of test failures per build cycle. An agentic workflow "
                "ingests structured failure logs from Jenkins CI/CD runs, uses LangGraph to orchestrate "
                "multi-step LLM reasoning chains, and produces clustered root-cause summaries with "
                "confidence scores and suggested remediation paths — compressing engineer triage time "
                "from hours to minutes."),
            2: ("Backend platform orchestrating distributed systems validation at 1.6 Tbps",
                "Core contributor to Ciena's internal developer platform — a Python service layer that "
                "orchestrates automated firmware and system-build validation across distributed networking "
                "hardware. Exposes REST APIs consumed by Jenkins CI/CD pipelines to trigger, monitor, and "
                "report on test runs across multiple hardware variants, reducing manual validation effort "
                "by 40–50%."),
            3: ("Research data APIs powering 118,000+ recipes and a 934-ingredient flavour knowledge base",
                "At the Complex Systems Laboratory, IIIT Delhi, built the backend data services underpinning "
                "two large-scale research knowledge bases. RecipeDB: a queryable API over 118,000+ recipes "
                "across 26 global regions. FlavorDB: data models and retrieval APIs for 934 natural "
                "ingredients and their flavour-molecule profiles, used by food scientists and researchers "
                "internationally."),
            4: ("Production APIs and backend systems scaled to 50,000+ active users",
                "Four years of independent backend engineering across startup and enterprise engagements. "
                "Designed and shipped production-grade Python and Flask backends from schema design through "
                "cloud deployment. Built automation-focused APIs that eliminated approximately 95% of "
                "clients' manual processing workloads. Systems deployed on GCP and Heroku, collectively "
                "serving 50,000+ active users in production."),
        }
        for proj_id, (tagline, desc) in proj_updates.items():
            proj = db.session.get(Project, proj_id)
            if proj:
                proj.tagline = tagline
                proj.description = desc

    db.session.commit()
    print("Content seeded.")

    # ── ADMIN USER ─────────────────────────────────────────────────────────────
    if AdminUser.query.count() == 0:
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD")
        if not password:
            print("WARNING: ADMIN_PASSWORD env var not set. Admin user not created.")
        else:
            create_admin(username, password)
            print(f"Admin user '{username}' created.")
    else:
        print("Admin user already exists — skipping.")

    print("Deploy seed complete.")
