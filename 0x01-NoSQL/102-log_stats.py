#!/usr/bin/env python3
""" a Python script that provides some stats about
Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs.nginx

    print(f"{db.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"\tmethod {method}: {db.count_documents({'method': method})}")
    Get_count = db.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{Get_count} status check")

    print('IPs:')
    pipe = [
            {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
    ]
    popular = list(nginx_logs.aggregate(pipe))
    for ip in popular:
        print('\t{}: {}'.format(ip['_id'], ip['count']))
