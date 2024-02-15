#!/usr/bin/python3
from flask import Flask

"""
This script will start a Flask web application
"""

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    This function will return a string
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    This function will return a string
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def route_with_text(text):
    """
    This function will return a string
    """
    if "_" in text:
        text_no_underscore = text.replace("_", " ")
        return "C " + text_no_underscore
    else:
        return "C " + text


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_with_text(text="is cool"):
    """
    This function will return a string
    """
    if "_" in text:
        text_no_underscore = text.replace("_", " ")
        return "Python " + text_no_underscore
    else:
        return "Python " + text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
