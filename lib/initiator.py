import requests
import json
from lib.handler import process_response
from lib.plugin.plugin import get_body_by_plugin, get_raw_body


def process_request(request_data, plugin):
    request = request_data['request']

    body = request.get('body', {}).get('raw', '')
    if 'response' in request_data:
        response_arg = request_data.get('response')[0]
        if response_arg['name'] != plugin:
            return {'status': 'resource not requested', 'plugin': response_arg['name']}
        body = get_body_by_plugin(response=response_arg, plugin=plugin)

    method = request['method']
    url = request.get('url', {}).get('raw', '')
    headers = {header['key']: header['value'] for header in request.get('header', [])}
    headers['Content-Type'] = 'application/json'

    # Make the HTTP request
    response = requests.request(method, url, headers=headers, data=json.dumps(body))

    processed_response = []
    json_response = json.loads(response.text)
    if response.status_code == 200:
        processed_response = process_response(json_response,
                                              get_raw_body(response=request_data.get('response')[0], plugin=plugin))

    return {
        'url': url,
        'body': body,
        'status_code': response.status_code,
        'response_body': json_response,
        'processed_response': processed_response
    }


def proces_individual_request(collection, plugin_id):
    results = []
    # Process a single request from the collection
    for request in collection:
        results.append(process_request(request_data=request, plugin=plugin_id))
    return results
