import logging
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from services.products import Products
from exceptions.exceptions import ApiException, ModeledApiException, Message

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.errorhandler(404)
def page_not_found(e):
    not_found_message = '404 Not Found: The requested URL was not found on the server'
    result = ModeledApiException(errors=[Message(message=not_found_message)])
    return jsonify(result)


@app.errorhandler(ApiException)
def invalid_api_usage(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


@app.route('/up/', methods=['GET'])
def up():
    return jsonify({"status": "happy"})


@app.route('/products/<string:product_id>/', methods=['GET', 'PUT'])
def get_product_info(product_id: str):
    if request.method == 'GET':
        result = Products().get_product_info(product_id)
        return Response(result.to_json(), status=200, mimetype='application/json')
    else:
        result = Products().update_product_price(json.loads(request.data), product_id)
        if result == 1:
            return Response(status=204, mimetype='application/json')
        else:
            raise ApiException(message=f'Unable to update price for product with product id {product_id}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
