import flask


def favicon() -> flask.Response:
    return flask.send_from_directory("static", "favicon.ico")
