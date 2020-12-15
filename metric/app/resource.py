from abc import ABC
from flask import request
from flask.json import jsonify


class Resource(ABC):
    # ____class method for resources____
    headers, body, file = [{}, {}, {}]

    # ** PROPERTY REQUESTS **
    @property
    def requests(self) -> dict:
        """
        ### REQUESTS
        ---
        this function is used as property from resource class to retrieve request from data
        like raw data json, form-data, query-string and even file upload.
        ---
        """
        _req = lambda: None

        if request.is_json:
            _req = request.json
        else:
            if bool(request.form):
                _req = request.form

                if bool(request.files) and isinstance(request.files, dict):
                    _req.upload = request.files
            elif bool(request.args):
                _req = request.args

        return _req

    def validation(self, variable, **kwargs):
        try:
            for k, v in kwargs:
                validate = v.split(',')

                # ____this section is checking the type validation.
                # validation available: numeric, string and json____
                if filter(lambda x: x == 'numeric', validate):
                    v = int(v)
                elif filter(lambda x: x == 'string', validate):
                    v = str(v)
                elif filter(lambda x: x == 'json', validate):
                    v = jsonify(v)
        except:
            pass
