import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance Proxy is Running!"

@app.route('/proxy', methods=['POST'])
def proxy():
    try:
        data = request.json
        url = data.get('url')
        headers = data.get('headers', {})
        params = data.get('params', {})
        payload = data.get('payload', {})
        method = data.get('method', 'GET')
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=payload if payload else None
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
