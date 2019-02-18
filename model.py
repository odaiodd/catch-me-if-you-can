# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE

from pymongo.mongo_client import MongoClient
import numpy as np
from datetime import datetime


class Storage:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.my_DB = self.db.get_collection("Ads DB")
        # self.user_list = self.db.get_collection("Users List")

    def add_my_db(self, ad_id, screen_id, encoding, face_id, time, img):
        self.my_DB.replace_one({'db_id': "COUNTER DOCUMENT NUMBER 0"}, {
            'ad_id': ad_id,
            'screen_id': screen_id,
            'encoding': encoding,
            'face_id': face_id,
            'time': time,
            'image': img.tolist()
        }, upsert=True)

    def clear_table(self):
        self.my_DB.delete_many({})

class Storage_store:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.my_DB = self.db.get_collection("Matches")
        # self.user_list = self.db.get_collection("Users List")

    def add_my_db(self, face_id, ad_id, store_id, img, time):
        self.my_DB.replace_one({'db_id': "COUNTER DOCUMENT NUMBER 0"}, {
            'ad_id': ad_id,
            'store_id': store_id,
            'face_id': face_id,
            'time': time,
            'image': img.tolist()
        }, upsert=True)

    def clear_table(self):
        self.my_DB.delete_many({})