#!/usr/bin/env python3
"""
Module to list all documents using pymongo
"""


def list_all(mongo_collection):
    """
    list_all - list all documents in a collection
    Args:
        mongo_collection (pymongo.collection): collection to list
    Returns:
        list of all documents in the collection
    """
    return [doc for doc in mongo_collection.find()]
