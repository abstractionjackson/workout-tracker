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

from workout_tracker.auth import load_logged_in_user, login_required
from workout_tracker.database import db_session
from workout_tracker.models import Exercise, User, Workout

bp = Blueprint("workout", __name__, url_prefix="/workout")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter_by(id=user_id).first()


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    error = None

    date = datetime.now()

    if error is None:
        workout = Workout(date=date, user_id=g.user.id)
        db_session.add(workout)
        try:
            db_session.commit()
        except BaseException as e:
            error = e
            flash(error)
        else:
            flash(f"Workout created.")
            return redirect(url_for("workout.edit", workout_id=workout.id))
    return redirect(url_for("workout.index"))


@bp.route("/")
@login_required
def index():
    # get all the workouts for the logged in user sorted by date in descending order
    user_id = g.user.id
    workouts = (
        db_session.query(Workout)
        .filter_by(user_id=user_id)
        .order_by(Workout.date.desc())
        .all()
    )
    return render_template("workout/index.html", workouts=workouts)


@bp.route("/<int:workout_id>")
@login_required
def single(workout_id):
    workout = db_session.query(Workout).filter_by(id=workout_id).first()
    # group the workout sets by exercise and order by order (property)
    set_workout_sets_by_exercise(workout)
    return render_template("workout/single.html", workout=workout)


def set_workout_sets_by_exercise(workout):
    sets_by_exercise = {}
    for s in workout.sets:
        if s.exercise_name not in sets_by_exercise:
            sets_by_exercise[s.exercise_name] = []
        sets_by_exercise[s.exercise_name].append(s)
        sets_by_exercise[s.exercise_name].sort(key=lambda x: x.order)
    workout.sets_by_exercise = sets_by_exercise


@bp.route("edit/<int:workout_id>", methods=("GET", "POST"))
@login_required
def edit(workout_id):
    session["workout_id"] = workout_id
    exercises = db_session.query(Exercise).all()
    workout = db_session.query(Workout).filter_by(id=workout_id).first()
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        workout.date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        db_session.commit()
    set_workout_sets_by_exercise(workout)
    return render_template("workout/edit.html", workout=workout, exercises=exercises)


@bp.route("/delete/<int:workout_id>", methods=("GET",))
@login_required
def delete(workout_id):
    workout = db_session.query(Workout).filter_by(id=workout_id).first()
    db_session.delete(workout)
    db_session.commit()
    flash("Workout deleted")
    return redirect(url_for("workout.index"))
