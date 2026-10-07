from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Binance වල ප්‍රධාන API ලිපිනයන්
BINANCE_API_BASE = "https://api.binance.com"
BINANCE_FUTURES_BASE = "https://fbinance.com" # හෝ fapi.binance.com

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    url = f"{BINANCE_API_BASE}/api/{path}"
    return forward_request(url)

@app.route('/fapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_fapi(path):
    url = f"https://fapi.binance.com/fapi/{path}"
    return forward_request(url)

def forward_request(url):
    # බ්‍රව්සරයෙන් හෝ බොට්ගෙන් එන headers සහ data Binance එකට හරවා යැවීම
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    return Response(resp.content, resp.status_code, headers)

@app.route('/')
def home():
    return "Binance Proxy is Running!"

if __name__ == '__main__':
    app.run()
