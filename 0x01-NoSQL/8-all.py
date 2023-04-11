#!/usr/bin/env python3
'''python function that lists all documents in a collection'''

def list_all(mongo_collection):
    cursor = mongo_collection.find()
    result = []
    for document in cursor:
        result.append(document)

    return result
