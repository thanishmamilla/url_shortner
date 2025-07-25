from flask import Flask, jsonify, request, redirect, abort, url_for
from .models import URLStore
from .utils import is_valid_url, generate_short_code

app = Flask(__name__)
store = URLStore()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400
    # Generate unique short code
    for _ in range(10):
        code = generate_short_code()
        if not store.exists(code):
            store.add(code, long_url)
            short_url = request.host_url.rstrip('/') + '/' + code
            return jsonify({"short_code": code, "short_url": short_url}), 201
    return jsonify({"error": "Could not generate unique short code"}), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    entry = store.get(short_code)
    if not entry:
        abort(404)
    store.increment_click(short_code)
    return redirect(entry['url'])

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    entry = store.get(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": entry['url'],
        "clicks": entry['clicks'],
        "created_at": entry['created_at']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)