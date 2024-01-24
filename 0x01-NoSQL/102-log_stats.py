#!/usr/bin/env python3
""" a Python script that provides some stats about
Nginx logs stored in MongoDB"""
from pymongo import MongoClient
from collections import Counter


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
    
    print("IPs:")

    ip_counts = Counter(log['ip'] for log in db.find())
    for ip, count in ip_counts.most_common(10):
        print(f"\t{ip}: {count}")
