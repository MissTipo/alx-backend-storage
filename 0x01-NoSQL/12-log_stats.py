#!/usr/bin/env python3
'''Log stats'''


from pymongo import MongoClient


if __name__== '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    logs = nginx.count_documents({})
    get = nginx.count_documents({'method' : 'GET'})
    post = nginx.count_documents({'method' : 'POST'})
    put = nginx.count_documents({'method' : 'PUT'})
    delete = nginx.count_documents({'method' : 'DELETE'})
    patch = nginx.count_documents({'method' : 'PATCH'})

    status =  nginx.count_documents({'$and': [{'method' : 'GET'}, {"path": "/status"}]})
    
    print('''{} logs
Methods:
    method GET: {}
    method POST: {}
    method PUT: {}
    method PATCH: {}
    method DELETE: {}
{} status check'''
          .format(logs, get, post, put, patch, delete, status)
          )

