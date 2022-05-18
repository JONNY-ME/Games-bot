from pymongo import MongoClient
from decouple import config


CLUSTER = config("CLUSTER")

client = MongoClient(CLUSTER)
db = client.usersdata

coll = db.users


def insert_user(_id, username, first_name, last_name, is_active=True, is_admin=False):
    user = {'_id': _id, 'username': username, 'first_name': first_name, 'last_name': last_name, 'is_active': is_active, 'is_admin': is_admin}
    coll.insert_one(user)

def get_user(_id):
    return coll.find_one({'_id': _id})

def get_all_users():
    return coll.find()

def get_all_active_users():
    return coll.find({'is_active': True})

def get_all_inactive_users():
    return coll.find({'is_active': False})

def get_all_users_count():
    return coll.count()

def get_all_active_users_count():
    return coll.count({'is_active': True})

def get_all_inactive_users_count():
    return coll.count({'is_active': False})

def get_user(query):
    return coll.find(query)

def get_admin():
    return coll.find({'is_admin': True})
