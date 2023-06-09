import json
from datetime import datetime
from bson import ObjectId


class Baseline(object):
    def __init__(self):
        pass

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        for element in self.__dict__:
            if type(self.__dict__[element]) is ObjectId:
                self.__dict__[element] = str(self.__dict__[element])
            if type(self.__dict__[element]) is datetime:
                self.__dict__[element] = str(self.__dict__[element])
        return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))

    def to_json_obj(self):
        obj = json.loads(self.to_json())
        obj.pop("_id")
        return obj
