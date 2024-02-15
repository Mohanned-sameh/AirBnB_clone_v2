#!/usr/bin/python3
"""
    Implementation of the State class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv
import models


type_of_storage = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """
    Implementation for the State.
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if type_of_storage == "db":
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete-orphan",
        )
    else:

        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals
            to the current State.id
            """
            cities_lista = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities_lista.append(city)
            return cities_lista
