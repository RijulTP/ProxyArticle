from flask import Flask, request, Response
import requests
from urllib.parse import urlparse, urlencode, urlunparse

app = Flask(__name__)

@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy_request():
    # Extract the URL from the request headers
    print("API")
    for header, value in request.headers.items():
        print(f"{header}: {value}")
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    url = request.headers.get('hex-url')

    if url is None:
        return Response('hex-url header is missing', status=400)

    # Parse the original request URL to extract query parameters
    parsed_url = urlparse(url)
    query_params = parsed_url.query

    # For GET requests, append query parameters from the original URL
    if request.method == 'GET':
        print("Get Request")
        query_params = urlencode(request.args)
        new_url = urlunparse(parsed_url._replace(query=query_params))
        data = None  # No data for GET requests
    else:
        new_url = url
        data = request.data

    method = request.method
    if request.method == 'GET':
        print("Get Request...")
        response = requests.get(url)
    elif request.method == 'POST':
        print("Executing POST request")
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url,headers=headers,data=data)
    elif request.method == 'PATCH':
        print("Executing PATCH request")
        headers = {'Content-Type': 'application/json'}
        response = requests.patch(url, headers=headers, data=data)
    elif request.method == 'DELETE':
        print("Executing DELETE request")
        response = requests.delete(url)
    elif request.method == 'PUT':
        print("Executing PUT request")
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, headers=headers, data=data)
    else:
        response = requests.request(method, new_url,headers=headers, data=data)

    # Return the response content with the appropriate content type and status code
    return Response(response.content, content_type=response.headers['Content-Type'], status=response.status_code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
