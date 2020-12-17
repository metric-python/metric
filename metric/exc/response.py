from flask import make_response


class HaltResponse(Exception):
    def __init__(self, errors, code):
        self.result = make_response(errors, code)
