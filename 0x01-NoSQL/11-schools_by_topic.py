#!/usr/bin/env python3
"""
Python function that returns the list of school
having a specific topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    This function returns the list of school having a specific topic.
    """
    list =  mongo_collection.find({"topics": topic})
    return list
