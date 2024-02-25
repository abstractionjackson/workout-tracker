from flask import Flask, render_template

from workout_tracker.database import db_session, init_db
from workout_tracker.auth import bp as auth_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="sqlite:///" + app.instance_path + "/workout_tracker.sqlite",
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    init_db()

    app.register_blueprint(auth_bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
