#!/usr/bin/env python3
"""
Module to list all documents using pymongo
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that returns the list of school having a specific topic

    Args:
        mongo_collection (pymongo.collection): collection to list
        topic (str): topic to search for
    
    Returns:
        list of all filterd documents in the collection
    """
    topic_search = {
        "topics": {
            "$elemMatch": {
                "$eq": topic
            }
        }
    }

    return [doc for doc in mongo_collection.find(topic_search)]
