from app import create_app, db
from app.models.admin import AdminUser
from app.models.content import About, Skill, Project, Experience, ContactMessage

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "AdminUser": AdminUser,
        "About": About,
        "Skill": Skill,
        "Project": Project,
        "Experience": Experience,
        "ContactMessage": ContactMessage,
    }


if __name__ == "__main__":
    app.run(debug=True, port=8080)
