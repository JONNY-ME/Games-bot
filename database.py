from pymongo import MongoClient
from decouple import config


CLUSTER = config("CLUSTER")

client = MongoClient(CLUSTER)
db = client.usersdata
