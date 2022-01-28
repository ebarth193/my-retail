from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/up/', methods=['GET'])
def up():
    return jsonify({"status": "happy"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
