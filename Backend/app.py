from flask import Flask, jsonify, request

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def get_prefix_matches(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        matches = []
        self._collect_words(node, prefix, matches)
        return matches
    
    def _collect_words(self, node, current_prefix, matches):
        if node.is_end_of_word:
            matches.append(current_prefix)
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_prefix + char, matches)

class WordSearchSystem:
    def __init__(self):
        self.trie = Trie()
        self.word_ranks = {}
    
    def load_words(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    word = line.strip()
                    if word and word not in self.word_ranks:
                        self.trie.insert(word)
                        self.word_ranks[word] = 0
        except FileNotFoundError:
            print(f"Warning: File {filename} not found. No words loaded.")
    
    def search_word(self, word):
        exists = self.trie.search(word)
        if exists:
            self.word_ranks[word] += 1
        return exists
    
    def auto_complete(self, prefix):
        matches = self.trie.get_prefix_matches(prefix)
        for word in matches:
            self.word_ranks[word] += 1
        matches.sort(key=lambda x: (-self.word_ranks[x], x))
        return matches
    
    def get_rank(self, word):
        return self.word_ranks.get(word, -1)

app = Flask(__name__)
wss = WordSearchSystem()
wss.load_words("Backend/words.txt")  # Load words on startup

@app.route('/load', methods=['GET'])
def load_words_route():
    wss.load_words("Backend/words.txt")
    return jsonify({"message": "Words reloaded successfully"})

@app.route('/search', methods=['GET'])
def search_word():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "Missing 'word' parameter"}), 400
    exists = wss.search_word(word)
    return jsonify({"exists": exists})

@app.route('/autocomplete', methods=['GET'])
def auto_complete():
    prefix = request.args.get('prefix')
    if not prefix:
        return jsonify({"error": "Missing 'prefix' parameter"}), 400
    suggestions = wss.auto_complete(prefix)
    return jsonify({"suggestions": suggestions})

@app.route('/rank', methods=['GET'])
def get_word_rank():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "Missing 'word' parameter"}), 400
    rank = wss.get_rank(word)
    return jsonify({"rank": rank})

if __name__ == '__main__':
    app.run(debug=True)
