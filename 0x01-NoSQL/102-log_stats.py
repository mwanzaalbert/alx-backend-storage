#!/usr/bin/env python3
"""
102-log_stats.py

This script provides statistics about Nginx logs stored in a MongoDB
collection. It connects to a MongoDB database, retrieves log entries, and
displays statistics about the requests, including HTTP methods and the most
frequent IP addresses.
"""

from pymongo import MongoClient
from collections import Counter


def print_log_stats(mongo_collection):
    """Prints statistics about Nginx logs."""
    # Count total logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents(
        {"method": method}) for method in methods}

    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")

    # Count GET requests for /status
    status_check = mongo_collection.count_documents({"method": "GET",
                                                     "path": "/status"})
    print(f"{status_check} status check")

    # Count the top 10 IPs
    ip_counts = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip in ip_counts:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    print_log_stats(logs_collection)
