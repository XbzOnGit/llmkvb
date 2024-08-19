import yaml
# provider, config.
swap_out_once_yaml_dict = {"request_generator":{"provider":"synthetic", 
"shape_generator":{"provider": "synthetic",
                  "request_interval_generator" : {"provider":"poisson", "qps": 5.0}, 
                   "request_length_generator":{"provider":"uniform", "min_tokens": 3000, "max_tokens": 3000, "prefill_to_decode_ratio": 300},
                   "num_requests" : 30,
                   "seed": 42,
                   },
"content_generator":{
    "new_string_generator":{"provider": "segment_new_string",
                  # min and max should be provided at run time as hard constrain.
                  # Only prefix.
                  # All random.
                  # This is for cache size.
                    "reuse_ratio_generator" : {"provider":"uniform", "left":0.0, "right":0.0},
                    "prefix_ratio_generator" : {"provider":"uniform", "left":1.0, "right":1.0},
                    "segment_length_generator": {"provider":"uniform", "left_per_length":0, "right_per_length":0.8},
                    "segment_interval_generator": {"provider": "uniform", "left_per_length":0, "right_per_length":0.8},
                    "max_following_segment_cnt": 4,
                    },
    "old_string_generator":{"request_selection_generator": {"provider": "uniform"},
                  "start_selection_generator": {"provider": "uniform"}},
},
"tokenizer_type": "transformers",
"content_type": "tokens",
"tokenizer_name": "bert-base-uncased",
"local_files_only" : True
}, "seed": 42,
"repeatition": 50,
"repeat_interval": 0.2,
}
with open("swap_out_once.yaml", "w") as f:
    yaml.dump(swap_out_once_yaml_dict, f)