from bson import ObjectId
import pymongo
import os 
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from datetime import datetime, timezone

load_dotenv()

mongo_uri = os.getenv("MONGO_URI",None)

if mongo_uri is None:
    raise ValueError("Database URI is not set in environment")

client = pymongo.MongoClient(host=mongo_uri)

db_name = os.getenv("DB_NAME",None)
if db_name is None:
    raise ValueError("Database is not set in environment")
db = client.get_database(db_name)
