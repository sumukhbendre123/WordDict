from flask import Flask, request, jsonify
from trie import Trie
import os

app = Flask(__name__)
trie = Trie()

@app.route('/load_words', methods=['POST'])
def load_words():
    file_path = request.json.get("path", "words.txt")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    with open(file_path, 'r') as f:
        for line in f:
            trie.insert(line.strip())
    return jsonify({"message": "Words loaded successfully"})

@app.route('/search', methods=['GET'])
def search_word():
    word = request.args.get("word")
    found = trie.search(word)
    return jsonify({"found": found})

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get("prefix")
    results = trie.auto_complete(prefix)
    return jsonify([{"word": word, "rank": rank} for word, rank in results])

@app.route('/increment', methods=['POST'])
def increment():
    word = request.json.get("word")
    trie.increment_rank(word)
    return jsonify({"message": f"Rank incremented for '{word}'"})

@app.route('/rank', methods=['GET'])
def get_rank():
    word = request.args.get("word")
    rank = trie.get_rank(word)
    return jsonify({"rank": rank})
