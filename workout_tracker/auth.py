import functools
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from workout_tracker.database import db_session
from workout_tracker.models import Exercise, User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/hello")
def hello():
    return "Hello, from Auth!"


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        error = None

        email = request.form["email"]
        password = request.form["password"]

        if not email:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                user = User(email=email, password=password)
                db_session.add(user)
                db_session.commit()
            except IntegrityError:
                error = f"Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = f"No user with email address {email}."
        elif not user.check_password(password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user.id
            session["exercise_names"] = [
                exercise.name for exercise in Exercise.query.all()
            ]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/profile")
@login_required
def profile():
    return render_template("auth/profile/index.html")


@bp.route("/profile/edit", methods=("GET", "POST"))
@login_required
def edit_profile():
    user = g.user

    if request.method == "POST":
        error = None

        # for each user prop, if key in form, update user prop
        for key in user.__dict__.keys():
            value = request.form.get(key)
            if value:
                if key == "date_of_birth":
                    value = datetime.strptime(value, "%Y-%m-%d")
                setattr(user, key, value)

        if error is None:
            db_session.commit()
            return redirect(url_for("auth.profile"))

        flash(error)

    return render_template("auth/profile/edit.html", user=user)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
