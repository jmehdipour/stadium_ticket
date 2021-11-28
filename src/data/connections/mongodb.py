from mongoengine import connect
from pymongo import ReturnDocument

from src.config import get_settings

backend_mongo = f"{get_settings().MONGO_URL}:{get_settings().MONGO_PORT}/{get_settings().MONGO_DB_NAME}?authSource=admin"

db_conn = connect(db=get_settings().MONGO_DB_NAME, host=backend_mongo)
mongo_db = db_conn[get_settings().MONGO_DB_NAME]


def counter(collection_name):
    result = mongo_db.counters.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result.get("count")
