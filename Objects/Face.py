# -*- coding: utf8 -*-
from datetime import datetime, timedelta
import os
import bson
import asyncio
from utils import get_mongodb
from Objects.Baseline import Baseline


class Face(Baseline):
    def __init__(self, eventId, landMarks=None):
        super().__init__()
        self._id = bson.objectid.ObjectId()
        self.eventId = eventId
        timestamp = (datetime.now() - datetime(1970, 1, 1)) / timedelta(microseconds=1)
        path = "faces/" + str(self._id)
        os.mkdir(path, 0o755)
        self.fileName = path + "/" + str(timestamp) . split(".")[0] + ".jpg"
        self.landMarks = landMarks
        self.faceDate = str(datetime.now())
        # db = get_mongodb()
        # db.face.insert_one(self.__dict__)

    def get_face_id(self):
        return self._id

    async def save_face(self):
        db = get_mongodb()
        db.face.insert_one(self.__dict__)

    def set_landmarks(self, landMarks):
        self.landMarks = landMarks
        db = get_mongodb()
        db.face.update({"_id": self._id},
                       {"$set": {"landMarks": landMarks.__dict__}})


class LandMark(Baseline):
    def __init__(self, right_eye, nose_bridge, chin, left_eye, nose_tip, left_eyebrow, bottom_lip, right_eyebrow,
                 top_lip):
        super().__init__()
        self.right_eye = right_eye
        self.nose_bridge = nose_bridge
        self.chin = chin
        self.left_eye = left_eye
        self.nose_tip = nose_tip
        self.left_eyebrow = left_eyebrow
        self.bottom_lip = bottom_lip
        self.right_eyebrow = right_eyebrow
        self.top_lip = top_lip

