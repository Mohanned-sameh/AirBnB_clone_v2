#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

"""
This script will start a Flask web application
"""

app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    """tear down"""
    storage.close()


@app.route("/states", strict_slashes=False)
def list_all_states():
    """
    this funtion will list all states
    """
    states = storage.all(State).values()
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def find_state(id):
    """
    this funtion will find a state by id
    """
    states = storage.all(State).values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html", state=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
