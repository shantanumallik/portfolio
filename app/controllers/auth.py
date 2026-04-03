from app.models.admin import AdminUser
from app import db
from flask_login import login_user, logout_user


def authenticate(username, password):
    user = AdminUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return True
    return False


def logout():
    logout_user()


def create_admin(username, password):
    if AdminUser.query.filter_by(username=username).first():
        raise ValueError(f"Admin user '{username}' already exists.")
    user = AdminUser(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def change_password(user, current_password, new_password):
    if not user.check_password(current_password):
        return False
    user.set_password(new_password)
    db.session.commit()
    return True
