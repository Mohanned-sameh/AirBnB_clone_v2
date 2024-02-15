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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
