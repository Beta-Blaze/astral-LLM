import os


def init_cfg(app) -> None:
    # SQL Alchemy config
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, '../instance/db.sqlite')

    # CORS config
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True