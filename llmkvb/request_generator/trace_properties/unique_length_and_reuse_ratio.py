import json
import sys


class TokenTrieNode:
    def __init__(self):
        self.children = {}

# Implement a trie token by token.
class TokenTrie:
    def __init__(self) -> None:
        self.root = TokenTrieNode()
        self.size = 0
    def insert(self, tokens: list):
        # Also return a hit length.
        hit_length = 0
        node = self.root
        for char in tokens:
            if char not in node.children:
                node.children[char] = TokenTrieNode()
                self.size += 1
            else:
                hit_length += 1
            node = node.children[char]
        return hit_length


def unique_prefix_token_length_and_reuse_ratio(trace_input_file, repeatition):
    trie = TokenTrie()
    total_hit_length = 0
    total_length = 0
    original_trace = []
    with open(trace_input_file, "r") as f:
        for line in f:
            req_dict = json.loads(line)
            tokens = req_dict["tokens"]
            original_trace.append(tokens)

    for _ in range(repeatition):
        for tokens in original_trace:
            hit_length = trie.insert(tokens)
            total_hit_length += hit_length
            total_length += len(tokens)
    reuse_ratio = total_hit_length / total_length
    return trie.size, reuse_ratio

if __name__ == '__main__':
    repeatition = 1
    if len(sys.argv) < 2:
        print("Usage: python3 unique_length_and_reuse_ratio.py trace_input_file [optional: repeatition]")
    elif len(sys.argv) == 3:
        repeatition = int(sys.argv[2])
    trace_input_file = sys.argv[1]
    unique_length, reuse_ratio = unique_prefix_token_length_and_reuse_ratio(trace_input_file, repeatition)
    print(f"unique_prefix_token_length: {unique_length}\nreuse_ratio: {reuse_ratio}")