#!/usr/bin/env python3
"""Function to update the topics of a school document."""


def update_topics(mongo_collection, name, topics):
    """Update the topics of a school document based on the school name."""
    mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )
