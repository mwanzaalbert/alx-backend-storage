#!/usr/bin/env python3
"""Contains a function to list all documents in a MongoDB collection."""


def list_all(mongo_collection):
    """List all documents in a collection."""
    return list(mongo_collection.find())
