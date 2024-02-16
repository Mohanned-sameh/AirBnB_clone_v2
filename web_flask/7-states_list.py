#!/usr/bin/python3
from flask import Flask, render_template
from models import storage

"""
    Flask setup
"""
app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """
    Closes the session
    """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    List of states
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


app.run(host="0.0.0.0", port=5000)
