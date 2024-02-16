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
        Initialize the BaseModel class.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        else:
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if "created_at" in kwargs.keys():
                kwargs["created_at"] = datetime.strptime(
                    kwargs["created_at"],
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
            if "updated_at" in kwargs.keys():
                kwargs["updated_at"] = datetime.strptime(
                    kwargs["updated_at"],
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
            if "__class__" in kwargs.keys():
                del kwargs["__class__"]
            self.__dict__.update(kwargs)

    def __str__(self):
        """
        Return the string representation of the BaseModel class.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__,
        )

    def save(self):
        """
        Update the attribute updated_at with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of __dict__ of the instance.
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in new_dict:
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
