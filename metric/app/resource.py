from abc import ABC
from flask import request
from flask import make_response, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import required


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

    def validation(self, **kwargs) -> dict:
        try:
            dict_validation = {}

            for k, v in kwargs.items():
                validate = v.split(',')
                tmp_validators = []

                if filter(lambda x: x == 'required', validate):
                    tmp_validators.append(required())

                if filter(lambda x: x == 'numeric', validate):
                    dict_validation[k] = IntegerField(k, validators=tmp_validators)
                else:
                    dict_validation[k] = StringField(k, validators=tmp_validators)
        except KeyError as err:
            print('asdflaksdjflaskdfj')
        else:
            class_name = f'{self.__class__.__name__.lower()}_forms_validation'
            validate = type(class_name, (FlaskForm, ), dict_validation)()

            if not validate.validate():
                return {
                    'errors': validate.errors,
                    'code': 422
                }
            else:
                return {
                    'errors': None
                }
