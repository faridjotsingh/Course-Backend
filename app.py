from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)
CORS(app)

# Load your cleaned data
df = pd.read_csv('data/courses.csv')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query missing"}), 400

    # Use fuzzy search to match courses
    titles = df['Courses Title'].tolist()
    matches = process.extract(query, titles, limit=len(titles))
    matched_titles = [match[0] for match in matches]
    results = df[df['Courses Title'].isin(matched_titles)]

    results = results.sort_values(by='rating', ascending=False)

    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)