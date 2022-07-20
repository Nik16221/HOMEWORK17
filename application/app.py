from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #создаем экземпляр SQLAlchemy


def create_app():
    """
    Настраиваем Flask и SQLAlchemy
    """
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        api = Api(app, version="1.0", description="Movies API")
        app.config["api"] = api
        from application import routes

        return app
