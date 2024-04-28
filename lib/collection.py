import os
import sys

from flask import jsonify
import requests
import json

collection_path = '/collection/'


def get_by_url_collection(collection_url):
    response = requests.get(collection_url)

    # Check if the request was successful
    if response.status_code == 200:
        collection_data = response.json()

        parse_collection(collection_data)
    else:
        print("Failed to fetch collection. Status code:", response.status_code)


def get_collection_by_file(collection):
    # Read the collection file
    with open(os.path.dirname(os.path.dirname(__file__))+collection_path+collection, 'r') as file:
        collection_data = json.load(file)

    # Process each request in the collection
    return parse_collection(collection_data)


def parse_collection(collection_data):
    print("Collection Name:", collection_data['info']['name'])
    print(collection_data)
    # Iterate through requests in the collection
    results = []
    for item in collection_data.get('item', []):
        item_obj = {}
        if 'request' in item:
            item_obj['request'] = item['request']
        if 'response' in item:
            item_obj['response'] = item['response']
        results.append(item_obj)

    return results
