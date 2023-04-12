#!/usr/bin/env python3
'''python function that lists all documents in a collection'''
import pymongo


def list_all(mongo_collection):
    '''lists all documents in a collection'''
    cursor = mongo_collection.find()
    result = []
    for document in cursor:
        result.append(document)

    return result
