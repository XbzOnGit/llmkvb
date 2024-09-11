import yaml
import math
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
    # The same total reuse ratio, different inside request reuse ratio.
    # config_gen(0.3, 0.6, 0.8, "uniform", 3000000, 2000, 4000, 5.0, 42, 300, "test_trace_cache_3000000_config.yaml")
    # config_gen(0.4, 0.3, 0.5, "uniform", 3001000, 2000, 4000, 5.0, 61, 300, "3000000_0240.yaml")
    # config_gen(0.4, 0.8, 0.84, "uniform", 3000000, 2000, 4000, 5.0, 61, 300, "3000000_0492.yaml")
    # config_gen(0.4, 0.9, 1.0, "uniform", 3000000, 2000, 4000, 5.0, 61, 300, "3000000_0570.yaml")
    # config_gen(0.4, 1.0, 1.0, "uniform", 3000000, 2000, 4000, 5.0, 61, 300, "3000000_0600.yaml")
    config_gen(0.24, 1.0, 1.0, "uniform", 3010000, 3000, 3000, 5.0, 61, 300, "3000000_0750.yaml")
    
