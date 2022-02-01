import logging
from flask import Flask
from flask import jsonify
from flask import Response as Response
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


@app.route('/products/<string:product_id>/', methods=['GET'])
def get_product_info(product_id: str):
    ps = Products()
    result = ps.get_product_info(product_id)
    return Response(result.to_json(), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
