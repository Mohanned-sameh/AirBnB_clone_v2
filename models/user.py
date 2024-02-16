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
    Implementation for the User.
    """

    __tablename__ = "users"
    if type_of_storage == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        places = []
        reviews = []

    @property
    def reviews(self):
        """
        Getter for the reviews.
        """
        review_list = []
        for review in models.storage.all(Review).values():
            if review.user_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def places(self):
        """
        Getter for the places.
        """
        place_list = []
        for place in models.storage.all(Place).values():
            if place.user_id == self.id:
                place_list.append(place)
        return place_list
