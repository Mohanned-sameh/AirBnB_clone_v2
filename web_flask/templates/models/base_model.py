#!/usr/bin/python3
"""
    This module defines the BaseModel class
"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    Base class for other classes to be used for the duration.
    """

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize public instance attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
            if "id" not in kwargs.keys():
                setattr(self, "id", str(uuid.uuid4()))
            time = datetime.now()
            if "created_at" not in kwargs.keys():
                setattr(self, "created_at", time)
            if "updated_at" not in kwargs.keys():
                setattr(self, "updated_at", time)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
        Return the print/str representation of the BaseModel class.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__,
        )

    def save(self):
        """
        Update updated_at with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return a dictionary representation of the BaseModel class.
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in new_dict.keys():
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """
        Delete the current instance from the storage.
        """
        models.storage.delete(self)

    def __repr__(self):
        """
        Return the string representation of the BaseModel class.
        """
        return self.__str__()
