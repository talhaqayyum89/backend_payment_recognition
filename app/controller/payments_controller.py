import json
import logging
import pandas as pd
from datetime import datetime
from flask import Blueprint, Response, jsonify, request
from flask_cors import cross_origin
from app.modules.payment_parser import get_predictions

payments_blueprint = Blueprint('payment',
                               __name__,
                               url_prefix='/payment',
                               )


@payments_blueprint.route('/', methods=['POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'multipart/form-data'])
# @auth.login_required
def index():
    return jsonify({"hello": "world"})


@payments_blueprint.route('/parser', methods=['POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'multipart/form-data'])
# @auth.login_required
def report():
    try:
        if 'file' not in request.files:
            return 'No file part'
        else:
            file = request.files['file']
        foo = file.filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{timestamp}_{foo}'
        file_path = 'uploads/' + filename
        file.save(file_path)
        df = pd.read_excel(file)
        # df = pd.read_excel(request_obj)
        response_obj = get_predictions(df)

        if not response_obj['status'] == 200:
            response_payload = json.dumps({"message": response_obj["predictions"]})
            return Response(response=response_payload,
                            status=response_obj['status'],
                            content_type='application/json')

        response_payload = json.dumps(response_obj)
        return Response(response=response_payload,
                        status=200,
                        content_type='application/json')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 400
