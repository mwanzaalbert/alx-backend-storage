#!/usr/bin/env python3
# Script to provide stats about Nginx logs stored in MongoDB

from pymongo import MongoClient

def main():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})

    # Print the total logs
    print(f"{total_logs} logs")

    # Count the number of documents for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count the number of documents for method=GET and path=/status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    main()
