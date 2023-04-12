#!/usr/bin/env python3
"""Write a Python script that provides some stats about Nginx
logs stored in MongoDB
"""
import pymongo
from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    """provides some stats about Nginx logs
    """
    total = mongo_collection.count_documents()
    print(f"{total} logs")
    
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    get_count =  mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{get_count} status check")



    if __name__ == "__main__":
        mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
        log_nginx_stats(mongo_collection)
