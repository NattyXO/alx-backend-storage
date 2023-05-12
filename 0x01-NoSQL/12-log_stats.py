#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://localhost:27017/')
    collection = client.logs.nginx

    total_logs = collection.count_documents({})
    print(f'{total_logs} logs')

    print('Methods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({'method': method})
        print(f'\tmethod {method}: {method_count}')

    status_count = collection.count_documents({'path': '/status'})
    print(f'{status_count} status check')

    print('IPs:')
    pipeline = [
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]
    result = collection.aggregate(pipeline)
    for doc in result:
        ip = doc['_id']
        count = doc['count']
        print(f'\t{ip}: {count}')


if __name__ == '__main__':
    log_stats()
