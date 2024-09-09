import sys
import json
from unique_length_and_reuse_ratio import TokenTrie
# Now only reduce though.
def correct_unique_token_length(trace_input_file, expected_unique_token_length):
    trie = TokenTrie()
    new_lines = []
    with open(trace_input_file, "r") as f:
        for line in f:
            req_dict = json.loads(line)
            size_before = trie.size
            assert size_before <= expected_unique_token_length
            if size_before == expected_unique_token_length:
                break
            hit_length = trie.insert(req_dict["tokens"])
            size_after = trie.size
            assert size_after >= size_before
            unique_len = len(req_dict["tokens"]) - hit_length
            assert size_after - size_before == unique_len
            if size_after >= expected_unique_token_length:
                # Delete part of the last request.
                # In reverse order.
                remove_cnt = size_after - expected_unique_token_length
                assert remove_cnt <= unique_len
                length_before = len(req_dict["tokens"])
                req_dict["tokens"] = req_dict["tokens"][:-remove_cnt]
                if len(req_dict["tokens"]) > 1:
                    # If == 1, just leave it.
                    # Change metadata.
                    if remove_cnt < req_dict["output_length"]:
                        # Remove output length.
                        req_dict["output_length"] -= remove_cnt
                    else:
                        # Remove all except one.
                        # At least one prefill token and one decode token.
                        req_dict["output_length"] = 1
                    new_lines.append(json.dumps(req_dict) + "\n")
                    
                print(f"Reduce {remove_cnt} tokens from the last request, from {length_before} to {len(req_dict['tokens'])}.")
                break
            else:
                assert size_after < expected_unique_token_length
                new_lines.append(line)
    with open(trace_input_file, "w") as f:
        for line in new_lines:
            f.write(line)

                

            
            

if __name__ == "__main__":
    assert len(sys.argv) == 3
    trace_input_file = sys.argv[1]
    expected_unique_token_length = int(sys.argv[2])
    correct_unique_token_length(trace_input_file, expected_unique_token_length)