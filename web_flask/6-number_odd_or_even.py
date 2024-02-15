#!/usr/bin/python3
from flask import Flask, render_template

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


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """
    This function will return a string
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    This function will return a string
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """
    This function will return a string
    """
    if n % 2 == 0:
        return render_template("6-number_odd_or_even.html", n=n, odd_or_even="even")
    else:
        return render_template("6-number_odd_or_even.html", n=n, odd_or_even="odd")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
