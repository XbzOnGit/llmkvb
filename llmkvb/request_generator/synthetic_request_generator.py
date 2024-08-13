from typing import List
from llmkvb.entities import Request
from llmkvb.request_generator.base_request_generator import BaseRequestGenerator
from llmkvb.request_generator.shape_generator import request_shape_generator_registry
from llmkvb.request_generator.content_generator.new_string import new_string_registry
from llmkvb.request_generator.content_generator.old_string import request_selection_registry
from llmkvb.request_generator.content_generator.old_string import start_selection_registry
from llmkvb.entities import Shape_Request
import random

class SyntheticRequestGenerator(BaseRequestGenerator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.shape_generator = \
            request_shape_generator_registry.RequestShapeGeneratorRegistry.get_from_str(self.config["shape_generator"]["provider"]\
                                                                                        , self.config["shape_generator"])
        self.new_string_generator = \
            new_string_registry.NewStringGeneratorRegistry.get_from_str(self.config["content_generator"]["new_string_generator"]["provider"], \
                                                                        self.config["content_generator"]["new_string_generator"])
        self.request_selection_generator = \
            request_selection_registry.RequestSelectionGeneratorRegistry.get_from_str(\
                self.config["content_generator"]["old_string_generator"]["request_selection_generator"]["provider"], \
                    self.config["content_generator"]["old_string_generator"]["request_selection_generator"])
        self.start_selection_generator = \
            start_selection_registry.StartSelectionGeneratorRegistry.get_from_str(\
                self.config["content_generator"]["old_string_generator"]["start_selection_generator"]["provider"], \
                    self.config["content_generator"]["old_string_generator"]["start_selection_generator"])
        self.vocab_no_special_dict = {key: value for key, value in self.tokenizer.get_vocab().items() if value not in self.tokenizer.all_special_ids}
        self.vocab_no_special_string_list = list(self.vocab_no_special_dict.keys())
    def gen_random_tokens(self, length: int):
        random_tokens = []
        for _ in range(length):
            random_tokens.append(random.choice(self.vocab_no_special_string_list))
        return random_tokens
    def generate_requests(self) -> List[Request]:
        # timestamp && tokens
        retval = []
        request_shapes : List[Shape_Request] = self.shape_generator.generate_requests()
        pool_size = 0
        for shape in request_shapes:
            arrived_at = shape.arrived_at
            input_length = shape.input_length
            output_length = shape.output_length
            new_string = self.new_string_generator.generate_new_string(input_length=input_length)
            prefix_length = new_string[0]
            segments = new_string[1]
            tokens = []
            # TODO: Pass more information into request_selection.
            if pool_size == 0:
                # All tokens are random.
                tokens.extend(self.gen_random_tokens(input_length))
            else:
                # Deal with prefix first.
                prefix_from_req_id = self.request_selection_generator.request_selection()
                copy_req = retval[prefix_from_req_id]
                copy_list = copy_req.tokens
                tokens.extend(copy_list[:prefix_length])
                # print("After copying prefix: token lentgh: ", len(tokens))
                # Deal with others.
                lastend = prefix_length - 1
                for seg in segments:
                    st = seg[0]
                    length = seg[1]
                    # Random for [lastend + 1, st - 1]
                    ranlen = st - lastend - 1
                    # print(f"ranlen in between {ranlen}")
                    tokens.extend(self.gen_random_tokens(ranlen))
                    # print("After random: token lentgh: ", len(tokens))
                    # Copy for [st, st + length - 1]
                    copy_req_id = self.request_selection_generator.request_selection()
                    copy_req = retval[copy_req_id]
                    copy_start_index = 0
                    if length <= len(copy_req.tokens):
                        copy_start_index = self.start_selection_generator.select(left=0, right=len(copy_req.tokens) - length)
                    else:
                        copy_start_index = self.start_selection_generator.select(left=0, right=len(copy_req.tokens) - 1)
                    copy_list = copy_req.tokens
                    # print(f"Copy from {copy_req_id}, {copy_start_index} : {copy_start_index + length} with length {length} to {st}: {st + length}")
                    # print(f"Choses req: {copy_req_id} with length {len(copy_list)}")
                    if len(copy_list) < length:
                        first_round = len(copy_list) - copy_start_index
                        tokens.extend(copy_list[copy_start_index:copy_start_index + first_round])
                        # print(f"After extend of first round with copy req < length, {len(tokens)}")
                        remaining_copy_cnt = length - first_round
                        while remaining_copy_cnt > len(copy_list):
                            tokens.extend(copy_list)
                            # print(f"After extend of middle rounds with copy req < length, {len(tokens)}")
                            remaining_copy_cnt -= len(copy_list)
                        tokens.extend(copy_list[:remaining_copy_cnt])
                        # print(f"After extend of last round with copy req < length, {len(tokens)}")
                    else:
                        tokens.extend(copy_list[copy_start_index:copy_start_index + length])
                        # print(f"After extend of copy req >= length, {len(tokens)}")
                    lastend = st + length - 1
                # The last random one for [lastend + 1, input_length - 1]
                ranlen = input_length - lastend - 1
                tokens.extend(self.gen_random_tokens(ranlen))
                # print(f"After update of last randoms {len(tokens)}")
            self.request_selection_generator.update()
            pool_size += 1
            retval.append(Request(arrived_at=arrived_at, tokens=tokens, output_length=output_length))
        return retval
        
        
            
        