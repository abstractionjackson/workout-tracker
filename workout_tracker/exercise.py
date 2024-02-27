from datetime import datetime
from sqlalchemy.exc import IntegrityError
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

from workout_tracker.auth import load_logged_in_user, login_required
from workout_tracker.database import db_session
from workout_tracker.models import Category, User, Workout, Exercise

bp = Blueprint("exercise", __name__, url_prefix="/exercise")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    error = None
    # get redirect url from the query params "redirect_to", the headers, or the create page
    redirect_to = request.args.get(
        "redirect_to", request.headers.get("Referer", url_for("exercise.create"))
    )

    if request.method == "POST":
        exercise_name = request.form["exercise_name"]
        try:
            db_session.add(Exercise(name=exercise_name))
            db_session.commit()
        except IntegrityError:
            error = f"Exercise {exercise_name} already exists."
        else:
            session["exercise_names"].append(exercise_name)
            flash(f"Exercise {exercise_name} created.")

            return redirect(redirect_to)

    if error:
        flash(error)

    return render_template("exercise/create.html", error=error, redirect_to=redirect_to)
