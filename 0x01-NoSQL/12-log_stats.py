#!/usr/bin/env python3
"""
Defines a function that provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def nginx_stats_check():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient()
    collec_nginx = client.logs.nginx

    # Count number of documents
    num_of_docs = collec_nginx.count_documents({})
    print("{} logs".format(num_of_docs))

    # Count methods
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods_list:
        method_count = collec_nginx.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))

    # Count status check
    status_count = collec_nginx.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_count))

    # Count top IPs
    top_ips = collec_nginx.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip in top_ips:
        print("\t{}: {}".format(ip['_id'], ip['count']))


if __name__ == "__main__":
    nginx_stats_check()
