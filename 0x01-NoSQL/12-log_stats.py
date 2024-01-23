#!/usr/bin/env
""" a Python script that provides some stats about
Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(mongodb://127.0.0.1:27017)
    db = client.logs.nginx

    print(f"{db.count_documents({})} logs")
    print("Methods:")
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"\tmethod {method}: {db.count_documents({'method': method})}")
    print(f"{db.count_documents({'method': 'GET', 'path': '/status'})} status check")
