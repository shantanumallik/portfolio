"""
One-time script to populate the portfolio with real CV data.
Run with: python seed_real.py
"""
from app import create_app, db
from app.models.content import About, Skill, Project, Experience

app = create_app()

with app.app_context():

    # ── ABOUT ──────────────────────────────────────────────────────────────────
    about = About.query.first() or About()
    about.hero_tagline   = "I build systems that think."
    about.hero_subtitle  = "Python · Agentic AI · Distributed Systems · Backend Engineering"
    about.bio = (
        "I am a versatile software engineer whose work spans backend platform engineering, "
        "Agentic AI development, and large-scale distributed systems. "
        "At Ciena I design and ship Python-based backend services and REST APIs that power "
        "CI/CD-backed internal platforms for automated validation of distributed networking gear "
        "running at up to 1.6 Tbps — cutting manual testing effort by ~40–50%. "
        "I love going deep: implementing AI-assisted failure triaging workflows that cluster root "
        "causes using LLM reasoning, building orchestration logic across heterogeneous hardware "
        "variants, and surfacing platform insights through Grafana dashboards. "
        "My earlier experience spans data engineering (Python, PySpark-style pipelines), "
        "large-scale knowledge-base APIs (118,000+ recipes, 934 flavour ingredients), and "
        "full-stack production systems serving 50,000+ users. "
        "I thrive on solving complex engineering problems — especially where AI meets systems design."
    )
    about.location      = "Gurugram, Haryana, India"
    about.email         = "me@shantanumallik.com"
    about.linkedin_url  = "https://www.linkedin.com/in/shantanumallik"
    about.github_url    = ""
    about.resume_url    = ""
    db.session.add(about)

    # ── SKILLS ─────────────────────────────────────────────────────────────────
    Skill.query.delete()

    skills = [
        # (name, category, proficiency, is_featured, order)

        # Python & Backend — primary focus
        ("Python",                  "Backend Engineering", 97, True,  0),
        ("REST API Design",         "Backend Engineering", 93, True,  1),
        ("Flask / FastAPI",         "Backend Engineering", 88, True,  2),
        ("PostgreSQL",              "Backend Engineering", 82, False, 3),
        ("Docker",                  "Backend Engineering", 80, False, 4),
        ("Linux",                   "Backend Engineering", 87, False, 5),

        # Agentic AI — second primary pillar
        ("Agentic AI Systems",      "Agentic AI",          93, True,  0),
        ("LangChain / LangGraph",   "Agentic AI",          89, True,  1),
        ("LLM Integration",         "Agentic AI",          87, True,  2),
        ("AI Failure Triaging",     "Agentic AI",          90, True,  3),
        ("RAG Pipelines",           "Agentic AI",          84, False, 4),
        ("Prompt Engineering",      "Agentic AI",          88, False, 5),

        # Platform & Validation — Ciena focus
        ("Test Automation",         "Platform & CI/CD",    93, True,  0),
        ("Jenkins CI/CD",           "Platform & CI/CD",    90, True,  1),
        ("Distributed Systems",     "Platform & CI/CD",    84, True,  2),
        ("Grafana",                 "Platform & CI/CD",    80, False, 3),
        ("TestRail",                "Platform & CI/CD",    78, False, 4),

        # Data Engineering
        ("Data Modeling",           "Data Engineering",    85, False, 0),
        ("Data Pipeline Design",    "Data Engineering",    83, False, 1),
        ("Large-Scale Data Analysis","Data Engineering",   80, False, 2),

        # Tooling & Cloud
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
    Experience.query.delete()

    experience = [
        # (company, role, start, end, description, technologies, order)
        (
            "Ciena",
            "Software Systems Engineer",
            "Jan 2025", "Present",
            (
                "Joined as an Engineering Intern and converted to full-time Software Systems Engineer — "
                "building the internal developer platform that validates distributed networking hardware "
                "operating at up to 1.6 Tbps. "
                "Design and ship Python-based backend services and REST APIs consumed by Jenkins CI/CD "
                "pipelines to automate firmware and system-build validation across multiple hardware "
                "variants — reducing manual testing effort by ~40–50%. "
                "Developed AI-assisted failure triaging workflows: an agentic system (LangChain/LangGraph) "
                "that ingests raw test failures, clusters root causes using LLM reasoning, and delivers "
                "structured debugging summaries to developers — compressing triage time from hours to minutes. "
                "Architected Grafana dashboards surfacing build-execution trends, test stability signals, "
                "and platform-health KPIs for engineering leadership. "
                "Own reusable orchestration services and abstractions used across the platform."
            ),
            "Python, LangChain, LangGraph, REST APIs, Jenkins, Grafana, TestRail, CI/CD, Git, Linux",
            0,
        ),
        (
            "Complex Systems Laboratory / Foodoscope",
            "Research Intern",
            "Jan 2024", "Jan 2025",
            (
                "Research Assistant at IIIT Delhi's Complex Systems Lab, building backend systems "
                "and data APIs for large-scale food, nutrition, and health knowledge bases. "
                "Key contributions: "
                "FlavorDB — APIs and data models for 934 natural ingredients across 36 categories and their flavour-molecule compositions; "
                "RecipeDB — data pipelines and querying layer for 118,000+ recipes spanning 26 global regions; "
                "DietRx — backend for a curated database linking dietary ingredients to clinical therapeutic evidence by diet-disease associations. "
                "Designed processing workflows for complex, heterogeneous scientific datasets enabling "
                "efficient querying, cross-dataset aggregation, and downstream analytics for research publications."
            ),
            "Python, REST APIs, Data Modeling, Data Pipeline Design, PostgreSQL, Large-Scale Data Processing",
            1,
        ),
        (
            "Freelance",
            "Software Engineer",
            "Apr 2019", "Apr 2023",
            (
                "Four years of end-to-end ownership across backend, APIs, database design, and "
                "cloud deployment for startups and enterprise clients. "
                "Delivered production-grade Python and Ruby on Rails systems serving 50,000+ active users. "
                "Built automation-heavy APIs that eliminated ~95% of manual processing effort for clients. "
                "Led major platform refactors (security hardening, performance tuning, dependency upgrades) "
                "and managed full deployment pipelines on GCP and Heroku. "
                "Specialised in rapid delivery — shipping core modules within tight timelines while "
                "maintaining long-term codebase quality."
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

    # ── PROJECTS ───────────────────────────────────────────────────────────────
    Project.query.delete()

    projects = [
        # (title, tagline, description, tech_stack, github, demo, image, featured, order)
        (
            "Agentic Failure Triage System",
            "LLM-powered root-cause clustering for CI/CD test failures",
            (
                "Built at Ciena to tackle the hardest part of large-scale hardware validation: "
                "making sense of thousands of test failures per build cycle. "
                "An agentic workflow ingests structured failure logs from Jenkins CI/CD runs, "
                "uses LangGraph to orchestrate multi-step LLM reasoning chains, and produces "
                "clustered root-cause summaries with confidence scores and suggested fix paths — "
                "all surfaced back to developers through the internal platform API. "
                "Compresses triage time from hours to minutes across multi-terabit hardware variants."
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
                "report on 1000s of test runs across hardware variants. "
                "Reduces manual testing effort by ~40–50%. "
                "Paired with Grafana dashboards I built to surface build-execution trends, "
                "flaky-test signals, and platform-wide health KPIs to engineering leadership."
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
                "RecipeDB: queryable API over 118,000+ recipes across 26 global regions with "
                "nutritional composition, ingredient co-occurrence, and regional cuisine analytics. "
                "FlavorDB: data models and retrieval APIs for 934 natural ingredients and their "
                "flavour molecule profiles — used by food scientists globally for flavour pairing research. "
                "Also built DietRx: a curated therapeutic evidence layer linking dietary ingredients "
                "to clinical diet–disease associations."
            ),
            "Python, REST APIs, Data Modeling, Data Pipeline Design, PostgreSQL",
            "", "", "", False, 2,
        ),
        (
            "Freelance Backend Systems",
            "Production APIs and platforms scaled to 50,000+ users",
            (
                "Four years of independent full-stack and backend engineering across startup and "
                "enterprise engagements. Highlights: "
                "built automation-first APIs that eliminated ~95% of clients' manual processing workloads; "
                "led Rails platform upgrades from legacy versions — hardening security, cutting "
                "response times, and modernising dependency chains; "
                "delivered complete Python + Flask backends from schema design through cloud deployment "
                "on GCP and Heroku, serving 50,000+ active users in production. "
                "Owned the full engineering lifecycle — solo, under commercial timelines."
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

    db.session.commit()

    # Verify
    print(f"About:      updated — '{About.query.first().hero_tagline}'")
    print(f"Skills:     {Skill.query.count()} rows")
    print(f"Experience: {Experience.query.count()} rows")
    print(f"Projects:   {Project.query.count()} rows")
    print("\nCategories:", sorted({s.category for s in Skill.query.all()}))
    print("Done.")
