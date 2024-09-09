import yaml
import math
'''

reuse_ratio:  
reuse ratio(in one request) * (1 - no reuse ratio(across requests)).  

unique prefix token length:  
trace_length * mean_length_of_one_request * (no reuse ratio(across requests) + (1 - no reuse ratio(across requests))
* (1 - reuse ratio(inside one request)).  
).  
'''
'''
request_generator:
  content_generator:
    new_string_generator:
      max_following_segment_cnt: 4
      no_reuse_probability: 0.0
      prefix_ratio_generator:
        left: 0.0
        provider: uniform
        right: 1.0
      provider: segment_new_string
      reuse_ratio_generator:
        left: 0.7
        provider: uniform
        right: 0.9
      segment_interval_generator:
        left_per_length: 0
        provider: uniform
        right_per_length: 0.8
      segment_length_generator:
        left_per_length: 0
        provider: uniform
        right_per_length: 0.8
    old_string_generator:
      request_selection_generator:
        provider: uniform
      start_selection_generator:
        provider: uniform
  content_type: tokens
  local_files_only: true
  provider: synthetic
  shape_generator:
    num_requests: 1000
    provider: synthetic
    request_interval_generator:
      provider: poisson
      qps: 5.0
    request_length_generator:
      max_tokens: 4000
      min_tokens: 4000
      prefill_to_decode_ratio: 400
      provider: uniform
    seed: 42
  tokenizer_name: bert-base-uncased
  tokenizer_type: transformers
seed: 42

'''

# Now length is always uniform, it can be fixed.
# So only zipf is not supported.
# FIXME: Only assume uniform or FIXED.
# FIXME: This generates with NO repeatition.
def config_gen(no_reuse_requests_ratio, min_reuse_ratio_inside_a_request,
               max_reuse_ratio_inside_a_request, copy_pattern, unique_prefix_token_length, 
               min_token_length, max_token_length, qps, seed, pd_ratio, output_file_name: str):
    assert no_reuse_requests_ratio >= 0 and no_reuse_requests_ratio <= 1
    assert min_reuse_ratio_inside_a_request >= 0 and min_reuse_ratio_inside_a_request <= 1
    assert max_reuse_ratio_inside_a_request >= 0 and max_reuse_ratio_inside_a_request <= 1
    assert min_reuse_ratio_inside_a_request <= max_reuse_ratio_inside_a_request
    assert unique_prefix_token_length >= 0
    assert min_token_length >= 0
    assert max_token_length >= 0
    assert min_token_length <= max_token_length
    # FIXME: Assume UNIFORM.
    mean_reuse_ratio_inside_a_request = (min_reuse_ratio_inside_a_request + max_reuse_ratio_inside_a_request) / 2
    expected_reuse_ratio = mean_reuse_ratio_inside_a_request * (1 - no_reuse_requests_ratio)
    # FIXME: Assume UNIFORM.
    mean_token_length = (min_token_length + max_token_length) / 2
    trace_length = unique_prefix_token_length / (mean_token_length 
                                                 * (no_reuse_requests_ratio + 
                                                    (1 - no_reuse_requests_ratio) * (1 - mean_reuse_ratio_inside_a_request)))
    # trace length ceil to int.
    trace_length = math.ceil(trace_length)
    new_string_generator_yaml_dict = {
        "max_following_segment_cnt": 4,
        "no_reuse_probability": no_reuse_requests_ratio,
        # FIXME: Assume only PREFIX.
        "prefix_ratio_generator": {
            "left": 1.0,
            "provider": "uniform",
            "right": 1.0,
        },
        "provider": "segment_new_string",
        "reuse_ratio_generator": {
            "left": min_reuse_ratio_inside_a_request,
            "provider": "uniform",
            "right": max_reuse_ratio_inside_a_request,
        },
        "segment_interval_generator": {
            "left_per_length": 0,
            "provider": "uniform",
            "right_per_length": 0.8,
        },
        "segment_length_generator": {
            "left_per_length": 0,
            "provider": "uniform",
            "right_per_length": 0.8,
        },
    }
    old_string_generator_yaml_dict = { 
        "request_selection_generator": {
        "provider": copy_pattern,
    },
        "start_selection_generator": {
            "provider": "uniform",
        },
    }
    shape_generator_yaml_dict = {
        "num_requests": trace_length,
        "provider": "synthetic",
        "request_interval_generator": {
            "provider": "fixed",
            "qps": qps,
        },
        # FIXME: Assume UNIFORM.
        "request_length_generator": {
            "max_tokens": min_token_length,
            "min_tokens": max_token_length,
            "prefill_to_decode_ratio": pd_ratio,
            "provider": "uniform",
        },
        "seed": seed
    }
    request_generator_yaml_dict = {
        "content_generator": {
            "new_string_generator": new_string_generator_yaml_dict,
            "old_string_generator": old_string_generator_yaml_dict,
        },
        "content_type": "tokens",
        "local_files_only": True,
        "provider": "synthetic",
        "shape_generator": shape_generator_yaml_dict,
        "tokenizer_name": "bert-base-uncased",
        "tokenizer_type": "transformers",
    }
    yaml_dict = {"metadata":{"expected_total_reuse_ratio": expected_reuse_ratio, "expected_unique_prefix_token_length":
                             unique_prefix_token_length},
                    "request_generator": request_generator_yaml_dict,
                             "seed": seed,
                             }
    # dump to yaml file.
    with open(output_file_name, 'w') as f:
        yaml.dump(yaml_dict, f)

if __name__ == '__main__':
    # no reuse ratio is 0.3
    # 0.7 * ((0.6 + 0.8)/2) = 0.49
    config_gen(0.3, 0.6, 0.8, "uniform", 3000000, 2000, 4000, 5.0, 42, 300, "test_trace_cache_3000000_config.yaml")
    
