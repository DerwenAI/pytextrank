#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, send_from_directory, url_for  # pylint: disable=E0401
from pathlib import PurePosixPath
import os

DOCS_ROUTE = "/docs/"
DOCS_FILES = "../site"
DOCS_PORT = 8000

APP = Flask(__name__, static_folder=DOCS_FILES, template_folder=DOCS_FILES)

APP.config["DEBUG"] = False
APP.config["MAX_CONTENT_LENGTH"] = 52428800
APP.config["SECRET_KEY"] = "Technically, I remain uncommitted."
APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3000


@APP.route(DOCS_ROUTE, methods=["GET"])
@APP.route(DOCS_ROUTE + "<path:path>", methods=["GET"], defaults={"path": None})
@APP.route(DOCS_ROUTE + "<path:path>", methods=["GET"])
def static_proxy (path=""):
    """Serve static files from the /site directory."""
    if not path:
        suffix = ""
    else:
        suffix = PurePosixPath(path).suffix

    if suffix not in [".css", ".js", ".map", ".png", ".svg", ".xml"]:
        path = os.path.join(path, "index.html")

    return send_from_directory(DOCS_FILES, path)


@APP.route("/index.html")
@APP.route("/home/")
@APP.route("/")
def home_redirects ():
    """Serve generated documentation microsite.

    See build.md for more details.
    """
    return redirect(url_for("static_proxy"))


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=DOCS_PORT, debug=True)
