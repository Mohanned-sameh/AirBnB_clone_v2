#!/usr/bin/python3
"""
    Implementation of the Amenity class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
import models
from sqlalchemy.orm import relationship
from os import getenv

type_of_storage = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """
    Implementation for the Amenities.
    """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    if type_of_storage == "db":
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            back_populates="amenities",
        )
    else:

        @property
        def place_amenities(self):
            """
            Returns the list of Amenity instances with amenity_id equals
            to the current Amenity.id
            """
            amenities = models.storage.all(Amenity)
            amenities_lista = []
            for amenity in amenities.values():
                if amenity.amenity_id == self.id:
                    amenities_lista.append(amenity)
            return amenities_lista
