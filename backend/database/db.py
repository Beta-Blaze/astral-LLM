import os

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_db(app):
    db.init_app(app)
    db.create_all()
