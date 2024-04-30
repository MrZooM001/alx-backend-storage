#!/usr/bin/env python3
"""
Module to update a document using pymongo
"""


def update_topics(mongo_collection, name, topics):
    """
    Function to update a document into a collection using pymongo
    and depending on kwargs
    Args:
        mongo_collection (pymongo.collection): collection to insert into
        name (str): name of the document to update
        topics (list): list of topics to update
    Returns:
        id of the inserted document
    """
    mongo_collection.update_many(
        {"name": name},
        {'$set': {"topics": topics}}
    )
