
shape_request_id_cnt = 0
class Shape_Request:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        global shape_request_id_cnt
        self.id = shape_request_id_cnt
        shape_request_id_cnt += 1