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


storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """
    Define the class City that inherits from BaseModel.
    """

    __tablename__ = "cities"
    if storage_type == "db":
        state_id = Column(
            String(60),
            ForeignKey("states.id"),
            nullable=False,
        )
        name = Column(
            String(128),
            nullable=False,
        )
        places = relationship(
            "Place",
            backref="cities",
            cascade="all, delete-orphan",
        )
    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """
            Returns the list of Place instances with city_id equals
            to the current City.id
            """
            places = models.storage.all(Place)
            list_places = []
            for place in places.values():
                if place.city_id == self.id:
                    list_places.append(place)
            return list_places
