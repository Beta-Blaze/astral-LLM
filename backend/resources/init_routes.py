from backend.resources.routes.static import *
from backend.resources.routes.pages import *


def init(app) -> None:
    app.add_url_rule('/favicon.ico', 'favicon', favicon, methods=['GET'])
    app.add_url_rule('/', 'index', index, methods=['GET'])
