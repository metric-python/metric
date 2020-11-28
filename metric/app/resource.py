from abc import ABCMeta
from flask import request
from flask.json import jsonify
from metric.app import APP


class Resource(metaclass=ABCMeta):

    # ____class method for resources____
    headers, body, file = [{}, {}, {}]

    # ** PROPERTY REQUESTS **
    @property
    def requests(self) -> dict:
        """
        ### Property
        property requests for resources
        Returns:
            object: object request in dict results
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
    
    def validation(self, **kwargs):
        try:
            for k, v in kwargs:
                validate = v.split(',')

                # ____check the type if string, number or json____
                if filter(lambda x: x == 'numeric'):                
                    v = int(v)
                elif filter(lambda x: x == 'string'):
                    v = str(v)
                elif filter(lambda x: x == 'json'):
                    v = jsonify(v)
        except:
            pass
