import unittest

from lib.collection import get_collection_by_file
from lib.handler import process_response
from lib.plugin.plugin import get_raw_body


class TestParsePluginValue(unittest.TestCase):
    def test_parse_plugin_value_no_args(self):
        response = {
            "custTxnRefNo": "ref_no_123",
            "status": "success",
            "message": "Payment Request Received"
        }
        request_data = get_collection_by_file(collection="testing.postman_collection.json")
        result = process_response(response, get_raw_body(response=request_data[0].get('response')[0],
                                                         plugin="testing_request_200"))
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
