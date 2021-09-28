from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import pymongo
import os
import pymongo.errors as pymon_err

from datetime import date, datetime, timedelta



mongo_uri = "mongodb+srv://admin:vYVcVL8ROCz4HyIQ@cluster0.xhchx.mongodb.net/cner_dev?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)  

# accessing the database  
DB_NAME = 'cner_dev'
database = client[DB_NAME]

bcrypt = Bcrypt()


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


def hash_password(password):

    return bcrypt.generate_password_hash(password)

def match_password(db_password, password):

    return bcrypt.check_password_hash(db_password, password)

def set_password_hash():
    collection_name = 'c12_annotators'
    new_collection = database[collection_name]

    all_users = new_collection.find()
    for user in all_users:

        hashedpass=hash_password("password")

        new_collection.update_many({"email": user["email"]}, {"$set": {"password": hashedpass}})


set_password_hash()
