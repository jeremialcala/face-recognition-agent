# -*- coding: utf8 -*-
from Objects.Baseline import Baseline
import bson
import asyncio
import json
from utils import get_mongodb
from datetime import datetime


class Event(Baseline):
    def __init__(self, start_date, event_type, status=0, status_date=datetime.now(), obs="",
                 faces=None, match=False, mrz=None, card=None):
        super().__init__()
        self._id = bson.objectid.ObjectId()
        self.startDate = str(start_date)
        self.type = event_type
        self.status = status
        self.statusDate = str(status_date)
        self.obs = obs
        self.faces = faces
        self.match = match
        self.mrz = mrz
        self.card = card
        asyncio.run(self.save_event())

    def get_id(self):
        return self._id

    async def save_event(self):
        db = get_mongodb()
        db.events.insert_one(self.__dict__)

    async def update(self, status, status_date, obs):
        self.status = status
        self.statusDate = str(status_date)
        self.obs = obs
        db = get_mongodb()
        db.events.update_one({"_id": self._id},
                         {"$set": {"status": self.status, "statusDate": self.statusDate, "obs": self.obs}})
        db.events_log.insert_one(EventLog(self._id, status, status_date, obs).__dict__)


class EventLog(Event):
    def __init__(self, event_id, status, status_date, obs):
        self._id = bson.objectid.ObjectId()
        self.eventId = event_id
        self.status = status
        self.statusDate = str(status_date)
        self.obs = obs
