from flask import Flask, render_template, session

from workout_tracker.database import db_session, init_db
from workout_tracker.auth import bp as auth_bp
from workout_tracker.workout import bp as workout_bp
from workout_tracker.exercise import bp as exercise_bp
from workout_tracker.set import bp as set_bp
from workout_tracker.models import Exercise


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="sqlite:///" + app.instance_path + "/workout_tracker.sqlite",
    )

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(set_bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
