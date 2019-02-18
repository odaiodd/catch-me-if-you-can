from time import sleep

import model
import settings
import numpy as np

storage = model.Storage(settings.HOST, settings.DB)
storage_stores = model.Storage_store(settings.HOST, settings.DB)


def inatialize_table():
    storage.create_table()


def clear_DB(*collections):
    for collection in collections:
        collection.drop()


# clear_DB(storage.my_DB)


def add_to_table(obj):
    args = [obj.ads_id, obj.screen_id, obj.encoding, obj.id, obj.time, obj.img]
    storage.add_my_db(*args)


def get_from_db_by_filter(collection_name, conditions):
    my_user_list = storage.db[collection_name]
    myData = my_user_list.find(conditions)
    for user in myData:
        print(user)


def clear_DB():
    storage.clear_table()


def initDB():
    pass

# clear_DB()
# storage_stores.clear_table()
