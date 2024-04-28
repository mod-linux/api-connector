from flask import Flask, jsonify, request
from lib.initiator import process_request
from lib.collection import get_collection_by_file
import traceback

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_global_exception(e):
    tb = traceback.format_exc()

    # Create response with error message and traceback
    response = {
        "error": str(e),
        "traceback": tb
    }

    return jsonify(response), 500


@app.route('/api/', methods=['POST'])
def get_postman_collection():
    try:
        if request.is_json:
            data = request.get_json()
            collect_data = get_collection_by_file(collection=data['collection'])
            result = process_request(request_data=collect_data[0], plugin=data['plugin_id'])
            return jsonify(result)
        return jsonify({'error': False})
    except FileNotFoundError:
        return jsonify({"error": "Collection file not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
