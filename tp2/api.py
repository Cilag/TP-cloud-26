from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/hello', methods=['GET'])
def hello():
    response = make_response(jsonify({
        'message': 'Hello from serverless API!',
        'status': 'success'
    }))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)