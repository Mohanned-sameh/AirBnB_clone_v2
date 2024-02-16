#!/usr/bin/python3
"""
    Define the class City.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import models
from models.place import Place
from sqlalchemy.orm import relationship
from os import getenv


type_of_storage = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """
    Define the class City that inherits from BaseModel.
    """

    __tablename__ = "cities"
    if type_of_storage == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete")
    else:
        state_id = ""
        name = ""
        places = []

        @property
        def state(self):
            """
            Getter for the state.
            """
            state = models.storage.get("State", self.state_id)
            return state
