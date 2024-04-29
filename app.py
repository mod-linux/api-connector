import traceback

from flask import Flask, jsonify, request

from lib.collection import get_collection_by_file
from lib.initiator import proces_individual_request

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
            return jsonify(proces_individual_request(collect_data, data['plugin_id'])), 200
        return jsonify({'error': False}), 500
    except FileNotFoundError:
        return jsonify({"error": "Collection file not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
