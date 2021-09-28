from pymongo import MongoClient
import pymongo
import os
import pymongo.errors as pymon_err
import random

from datetime import date, datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

mongo_uri = "mongodb+srv://admin:vYVcVL8ROCz4HyIQ@cluster0.xhchx.mongodb.net/cner_dev?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)  

# accessing the database  
DB_NAME = 'cner_dev'
database = client[DB_NAME]




def rename_collection(old_name, new_name):

    # print('database: ', database)

    # access collection of the database  
    coll_1 = database[old_name] 

    # renaming the collection 
    coll_1.rename(new_name, dropTarget = True) 
    
    result = database.collection_names() 
    for collect in result: 
        print(collect)


# rename_collection("Clusters","clusters")

def create_c12_clusters():
    collection_name = 'c12_clusters'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("cluster_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "cluster_id"  : 1,
        "cluster_name"       : 1,
        "batch_id"        : 1,
        "created_at"    : current_datetime,
        "updated_at"    : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False

def create_c12_files():
    collection_name = 'c12_files'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("file_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "file_id"           : 1,
        "file_data"         : None,
        "assigned_status"   : None,
        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False

def create_c12_batch():
    collection_name = 'c12_batches'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("batch_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "batch_id"           : 1,
        "file_id"         : None,
        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False

def create_c12_pages():
    collection_name = 'c12_pages'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("page_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "page_id"           : 1,
        "batch_id"         : 1,
        "page_data"        : None,
        "file_id"          : 1,
        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False


def create_c12_pages():
    collection_name = 'c12_pages'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("page_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "page_id"           : 1,
        "batch_id"         : 1,
        "page_data"        : None,
        "file_id"          : 1,
        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False


def create_c12_annotations():
    
    collection_name = 'c12_annotations'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("annotation_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "annotation_id"           : 1,
        "annotator_id"         : 1,
        "annotation_data"        : None,
        "page_id"          : 1,
        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False



def create_c12_annotators():
    
    collection_name = 'c12_annotators'
    new_collection = database[collection_name]

    database[collection_name].create_index([
        ("annotator_id", pymongo.ASCENDING)
    ], unique = True)


    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
  
    user_gift_entry_dict = {
        "annotator_id"           : 1,
        "annotator_name"         : "rajacsp",
        "cluster_id"        : None,
        "password"          : None,
        "email"          : "raja@tactii.com",

        "created_at"        : current_datetime,
        "updated_at"        : current_datetime,
    }

    try:
        x = new_collection.insert_one(user_gift_entry_dict)
        print(x)

        return True
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')

        return False

def populate_dummy_annotator_data():

    collection_name = 'c12_annotators'
    new_collection = database[collection_name]

    current_datetime = datetime.now()

    name_list = ['ajesh','talha','vedha','prakash','ana']

    for i in range(5):


        user_gift_entry_dict = {
            "annotator_id"           : i+6,
            "annotator_name"         : name_list[i],
            "cluster_id"        : random.randint(1,3),
            "password"          : "password",
            "email"          : f"{name_list[i]}@tactii.com",

            "created_at"        : current_datetime,
            "updated_at"        : current_datetime,
        }

        try:
            x = new_collection.insert_one(user_gift_entry_dict)
            print(x)

        except pymon_err.DuplicateKeyError as e:
            # print(e)
            print('Duplicate Error')

            return False

def populate_dummy_batches_data():

    collection_name = 'c12_batches'
    new_collection = database[collection_name]

    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
    
    
    for i in range(5):

        file_id = [x for x in range((i)*5,(i+1)*5)]

        user_gift_entry_dict = {
            "batch_id"      : i+1,
            "file_id"       : file_id,
            "created_at"    : current_datetime,
            "updated_at"    : current_datetime,
        }

        try:
            x = new_collection.insert_one(user_gift_entry_dict)
            print(x)

        except pymon_err.DuplicateKeyError as e:
            # print(e)
            print('Duplicate Error')

            return False

def populate_dummy_cluster_data():

    collection_name = 'c12_clusters'
    new_collection = database[collection_name]

    # database[collection_name].create_index([
    #     ("gift_id", pymongo.ASCENDING),
    #     ("userid", pymongo.ASCENDING),
    # ], unique = True)


    current_datetime = datetime.now()
    
    for i in range(2):


        user_gift_entry_dict = {
            "cluster_id"  : i+2,
            "cluster_name"       : i+2,
            "batch_id"        : 1,
            "created_at"    : current_datetime,
            "updated_at"    : current_datetime,
        }

        try:
            x = new_collection.insert_one(user_gift_entry_dict)
            print(x)

        except pymon_err.DuplicateKeyError as e:
            # print(e)
            print('Duplicate Error')

            return False



if __name__ == '__main__':

    # create_c12_annotators()

    # populate_dummy_annotator_data()

    # populate_dummy_cluster_data()

    # populate_dummy_batches_data()

    pass
