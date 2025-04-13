from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
json_path = os.path.join(project_root, 'movies.json')

@app.route('/')
def home():
    return "✅ Suvie backend is running!"

@app.route('/movies')
def get_movies():
    if not os.path.exists(json_path):
        return jsonify({"error": "movies.json not found"}), 404

    try:
        with open(json_path, 'r') as f:
            movies = json.load(f)
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)