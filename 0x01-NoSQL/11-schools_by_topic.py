#!/usr/bin/env python3
"""Function to return a list of schools with a specific topic."""


def schools_by_topic(mongo_collection, topic):
    """Return a list of schools that have a specific topic."""
    return list(mongo_collection.find({"topics": topic}))
