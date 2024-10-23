#!/usr/bin/env python3
"""Function to insert a new document into a MongoDB collection."""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document into a collection and return the new _id."""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
