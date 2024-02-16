#!/usr/bin/python3
"""This is the state class"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state")

    if os.getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            """getter attribute cities that returns the list of City instances"""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

    else:
        cities = relationship("City", backref="state", cascade="all, delete")
