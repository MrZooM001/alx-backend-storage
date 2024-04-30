#!/usr/bin/env python3
"""
Module to insert a document using pymongo
"""


def insert_school(mongo_collection, **kwargs):
    """
    Function to insert a document into a collection using pymongo
    and depending on kwargs
    Args:
        mongo_collection (pymongo.collection): collection to insert into
        **kwargs (dict): document to insert
    Returns:
        id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
