import requests
from lib.plugin.plugin import get_body_by_plugin, get_raw_body
from lib.handler import process_response


def process_request(request_data, plugin):
    request = request_data['request']
    # Process a single request from the collection
    method = request['method']
    url = request.get('url', {}).get('raw', '')
    headers = {header['key']: header['value'] for header in request.get('header', [])}
    body = request.get('body', {}).get('raw', '')
    if 'response' in request_data:
        body = get_body_by_plugin(response=request_data.get('response')[0], plugin=plugin)

    # Make the HTTP request
    response = requests.request(method, url, headers=headers, data=body)

    dummy_response = {
        "custTxnRefNo": "ref_no_123",
        "status": "success",
        "message": "Payment Request Received"
    }

    processed_response = process_response(dummy_response,
                                          get_raw_body(response=request_data.get('response')[0], plugin=plugin))

    return {
        'url': url,
        'body': body,
        'status_code': response.status_code,
        'response_body': response.text,
        'processed_response': processed_response
    }