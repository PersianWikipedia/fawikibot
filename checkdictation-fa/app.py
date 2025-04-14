#!/usr/bin/env python3

from flask import Flask, Response
from zz_checkDictation_cmd import run


app = Flask(__name__)


@app.route("/check/<path:page>")
def check(page):
    result = "{}"
    result = run(page)

    response = Response(result, content_type="application/json;charset=utf8")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    app.run(threaded=True)
