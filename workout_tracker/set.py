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
from workout_tracker.models import Category, User, Workout, Exercise, Set

bp = Blueprint("set", __name__, url_prefix="/set")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    error = None
    workout_id = session["workout_id"]
    exercise_name = request.args.get("exercise_name") or request.form.get(
        "exercise_name"
    )
    sets = (
        db_session.query(Set)
        .filter_by(workout_id=workout_id, exercise_name=exercise_name)
        .all()
    )

    if request.method == "POST":
        reps = request.form["reps"]
        weight = request.form["weight"]
        notes = request.form["notes"]

        new_set = Set(
            workout_id=workout_id,
            exercise_name=exercise_name,
            order=len(sets) + 1,
            reps=reps,
            weight=weight,
            notes=notes,
        )
        db_session.add(new_set)
        db_session.commit()
        sets.append(new_set)

    set_order = None
    current_weight = None
    if len(sets) > 0:
        set_order = len(sets) + 1
        current_weight = sets[-1].weight
    return render_template(
        "set/create.html",
        sets=sets,
        exercise_name=exercise_name,
        set_order=set_order or 1,
        current_weight=current_weight,
        error=error,
        workout_id=workout_id,
    )


@bp.route("/edit/<int:set_id>", methods=["GET", "POST"])
@login_required
def edit(set_id):
    error = None
    set = db_session.query(Set).filter_by(id=set_id).first()

    if request.method == "POST":
        reps = request.form["reps"]
        weight = request.form["weight"]
        notes = request.form["notes"]

        set.reps = reps
        set.weight = weight
        set.notes = notes
        db_session.commit()

        flash("Set updated successfully")

        return redirect(url_for("workout.edit", workout_id=set.workout_id))

    return render_template("set/edit.html", set=set, error=error)
