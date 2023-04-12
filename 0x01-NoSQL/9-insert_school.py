#!/usr/bin/env python3
"""
Python function that inserts a new document in a collection based on kwargs
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    This function inserts a new document in a mongo collection
    based on the given keyword arguments.
    """
    res = mongo_collection.insert_one(kwargs)
    new_id = res.inserted_id

    return new_id
