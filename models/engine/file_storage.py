#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of objects.

        Return a dictionary of all objects in __objects. If a class is
        specified, return a dictionary of all objects of that class in
        __objects.
        """
        if cls is not None:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(d, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                for k, v in d.items():
                    cls = v["__class__"]
                    self.__objects[k] = eval(cls)(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Deserialize the JSON file to objects."""
        self.reload()
