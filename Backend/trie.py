class TrieNode:
    def __init__(self):
        self.children = {}
        self.rank = 0
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end_of_word = True

    def search(self, word):
        node = self._traverse(word)
        return node.is_end_of_word if node else False

    def auto_complete(self, prefix):
        node = self._traverse(prefix)
        results = []
        if node:
            self._dfs(node, prefix, results)
        return sorted(results, key=lambda x: -x[1])

    def increment_rank(self, word):
        node = self._traverse(word)
        if node and node.is_end_of_word:
            node.rank += 1

    def get_rank(self, word):
        node = self._traverse(word)
        return node.rank if node and node.is_end_of_word else None

    def _dfs(self, node, prefix, results):
        if node.is_end_of_word:
            results.append((prefix, node.rank))
        for ch, next_node in node.children.items():
            self._dfs(next_node, prefix + ch, results)

    def _traverse(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
