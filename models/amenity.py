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
    Implementation for the Amenity.
    """

    __tablename__ = "amenities"
    if type_of_storage == "db":
        name = Column(String(128), nullable=False)
        place_amenities = Table(
            "place_amenity",
            Base.metadata,
            Column(
                "place_id",
                String(60),
                ForeignKey("places.id"),
                primary_key=True,
                nullable=False,
            ),
            Column(
                "amenity_id",
                String(60),
                ForeignKey("amenities.id"),
                primary_key=True,
                nullable=False,
            ),
        )
        place = relationship(
            "Place",
            secondary=place_amenities,
            viewonly=False,
            back_populates="amenities",
        )
    else:
        name = ""

        @property
        def place(self):
            """
            Getter for the place.
            """
            place_list = []
            for place in models.storage.all(Place).values():
                if place.amenity_id == self.id:
                    place_list.append(place)
            return place_list

        @property
        def place_amenities(self):
            """
            Getter for the place_amenities.
            """
            place_amenities_list = []
            for place_amenity in models.storage.all(Place).values():
                if place_amenity.amenity_id == self.id:
                    place_amenities_list.append(place_amenity)
            return place_amenities_list
