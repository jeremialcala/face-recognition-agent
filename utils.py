import pymongo
import logging
from os import environ
from pymongo import errors


logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='{"dtTimeStamp": "%(asctime)s", "level": "%(levelname)s", '
                           '"function": "%(funcName)s()", "msg": "%(message)s"}')
log = logging.getLogger()


def get_mongodb():
    log.info("connecting to the database")
    db = None
    try:
        uri_mdb = environ.get("MONGOHOST")
        db = pymongo.MongoClient(uri_mdb)["FACES"]
    except errors.OperationFailure as e:
        log.error(str(e.args))
        return None
    except errors.ServerSelectionTimeoutError as e:
        log.error(str(e.args))
        return None
    finally:
        log.info("connected to the database")
        return db