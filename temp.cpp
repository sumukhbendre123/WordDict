#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;


struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isEndOfWord = false;
};


class Trie {
private:
    TrieNode* root;

    void collectWords(TrieNode* node, string& current, vector<string>& results) {
        if (node->isEndOfWord) results.push_back(current);
        for (auto& kv : node->children) { 
            char ch = kv.first;
            TrieNode* child = kv.second;
            current.push_back(ch);
            collectWords(child, current, results);
            current.pop_back();
        }
    }
    

public:
    Trie() : root(new TrieNode()) {}

    void insert(const string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (!curr->children.count(c))
                curr->children[c] = new TrieNode();
            curr = curr->children[c];
        }
        curr->isEndOfWord = true;
    }

    bool search(const string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (!curr->children.count(c)) return false;
            curr = curr->children[c];
        }
        return curr->isEndOfWord;
    }

    vector<string> getPrefixMatches(const string& prefix) {
        vector<string> results;
        TrieNode* curr = root;
        for (char c : prefix) {
            if (!curr->children.count(c)) return results;
            curr = curr->children[c];
        }
        string current = prefix;
        collectWords(curr, current, results);
        return results;
    }
};


class WordSearchSystem {
    Trie trie;
    unordered_map<string, int> wordRanks;

public:
    // 1. Load words from file
    void loadWords(const string& filename) {
        ifstream file(filename);
        string word;
        while (getline(file, word)) {
            if (!word.empty() && !wordRanks.count(word)) {
                trie.insert(word);
                wordRanks[word] = 0;
            }
        }
    }

    // 2. Search with rank increment
    bool searchWord(const string& word) {
        bool exists = trie.search(word);
        if (exists) wordRanks[word]++;
        return exists;
    }

    // 3. Auto-complete with ranking
    vector<string> autoComplete(const string& prefix) {
        vector<string> matches = trie.getPrefixMatches(prefix);
        
        // Update ranks and prepare for sorting
        for (auto& word : matches)
            wordRanks[word]++;
        
        sort(matches.begin(), matches.end(), 
            [this](const string& a, const string& b) {
                return wordRanks[a] != wordRanks[b] ? 
                       wordRanks[a] > wordRanks[b] : 
                       a < b;
            });
        
        return matches;
    }

    // 4. Rank management
    void incrementRank(const string& word) {
        if (wordRanks.count(word)) wordRanks[word]++;
    }

    int getRank(const string& word) {
        return wordRanks.count(word) ? wordRanks[word] : -1;
    }
};
int main() {
    WordSearchSystem wss;
    
    // Load words from file
    wss.loadWords("Backend/words.txt");
    
    // Auto-complete example
    vector<string> suggestions = wss.autoComplete("he");
    cout << "Suggestions: ";
    for (const auto& word : suggestions) 
        cout << word << " ";
    
    // Search example
    bool found = wss.searchWord("hello");
    cout << "\n'hello' " << (found ? "found" : "not found");
    
    // Get rank example
    cout << "\nRank of 'hello': " << wss.getRank("hello");
    
    return 0;
}
