#!/usr/bin/env python3
"""
15. Log stats - new version
"""
from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    """provides some stats about Nginx logs
    """
    total = mongo_collection.estimated_document_count()
    print(f"{total} logs")
    
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    get_count =  mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{get_count} status check")

    print("IPs:")
    IPs = mongo_collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for IP in IPs:
        count = IP.get("count")
        address = IP.get("ip")
        print("\t{}: {}".format(address, count))


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_nginx_stats(mongo_collection)
