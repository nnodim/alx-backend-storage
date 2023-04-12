#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    function to list all doc in a collection
    Return an empty list if no document in the collection
    """
    if not mongo_collection:
        return []
    docs = []
    for doc in mongo_collection.find():
        docs.append(doc)
    return docs
