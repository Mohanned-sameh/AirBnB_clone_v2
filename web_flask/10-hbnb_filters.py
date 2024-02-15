#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

"""
This script will start a Flask web application
"""

app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    """tear down"""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def show_page():
    """
    this funtion will show the page
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
