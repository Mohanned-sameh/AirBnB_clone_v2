#!/usr/bin/python3
"""
    Implementation of the User class which inherits from BaseModel
"""
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from os import getenv

type_of_storage = getenv("HBNB_TYPE_STORAGE")


class User(BaseModel, Base):
    """
    Definition of the User class
    """

    __tablename__ = "users"
    email = Column(
        String(128),
        nullable=False,
    )
    password = Column(
        String(128),
        nullable=False,
    )
    first_name = Column(
        String(128),
        nullable=True,
    )
    last_name = Column(
        String(128),
        nullable=True,
    )
    if type_of_storage == "db":
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete-orphan",
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan",
        )
    else:

        @property
        def places(self):
            """
            Returns the list of Place instances with user_id equals
            to the current User.id
            """
            places = models.storage.all(Place)
            places_lista = []
            for place in places.values():
                if place.user_id == self.id:
                    places_lista.append(place)
            return places_lista

        @property
        def reviews(self):
            """
            Returns the list of Review instances with user_id equals
            to the current User.id
            """
            reviews = models.storage.all(Review)
            reviews_lista = []
            for review in reviews.values():
                if review.user_id == self.id:
                    reviews_lista.append(review)
            return reviews_lista
