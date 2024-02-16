#!/usr/bin/python3
"""
    Define the class Place.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models
from os import getenv

type_of_storage = getenv("HBNB_TYPE_STORAGE")

if type_of_storage == "db":
    place_amenity = Table(
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


class Place(BaseModel, Base):
    """
    Define the class Place that inherits from BaseModel.
    """

    __tablename__ = "places"
    if type_of_storage == "db":
        city_id = Column(
            String(60),
            ForeignKey("cities.id"),
            nullable=False,
        )
        user_id = Column(
            String(60),
            ForeignKey("users.id"),
            nullable=False,
        )
        name = Column(
            String(128),
            nullable=False,
        )
        description = Column(
            String(1024),
            nullable=True,
        )
        number_rooms = Column(
            Integer,
            nullable=False,
            default=0,
        )
        number_bathrooms = Column(
            Integer,
            nullable=False,
            default=0,
        )
        max_guest = Column(
            Integer,
            nullable=False,
            default=0,
        )
        price_by_night = Column(
            Integer,
            nullable=False,
            default=0,
        )
        latitude = Column(
            Float,
            nullable=True,
        )
        longitude = Column(
            Float,
            nullable=True,
        )
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan",
        )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities",
            cascade="all",
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0

        @property
        def reviews(self):
            """
            Returns the list of Review instances with place_id equals
            to the current Place.id
            """
            reviews = models.storage.all(Review)
            reviews_lista = []
            for review in reviews.values():
                if review.place_id == self.id:
                    reviews_lista.append(review)
            return reviews_lista

        @property
        def amenities(self):
            """
            Returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
            """
            amenities = models.storage.all(Amenity)
            amenities_lista = []
            for amenity in amenities.values():
                if amenity.id in self.amenity_ids:
                    amenities_lista.append(amenity)
