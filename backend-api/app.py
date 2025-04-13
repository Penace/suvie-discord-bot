from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# This finds the root of your suvie-bot project, no matter what
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 🔍 Resolve absolute path to movies.json at the project root
json_path = os.path.join(project_root, 'movies.json')

print("🧭 Current Working Directory:", os.getcwd())
print("📦 Flask File Location:", os.path.dirname(__file__))
print("📂 Resolved movies.json Path:", json_path)

@app.route('/')
def home():
    return "✅ Suvie backend is running!"

@app.route('/movies')
def get_movies():
    print("🔍 /movies endpoint hit")

    if not os.path.exists(json_path):
        print("❌ movies.json not found at expected path.")
        return jsonify({"error": "movies.json not found"}), 404

    try:
        with open(json_path, 'r') as f:
            movies = json.load(f)
        return jsonify(movies)
    except Exception as e:
        print("🔥 Error reading movies.json:", e)
        return jsonify({"error": "Failed to read movies.json"}), 500

if __name__ == '__main__':
    print("🚀 Suvie backend started")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)