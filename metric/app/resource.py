from abc import ABC

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class Resource(ABC):
    """
    Base class resource, used as parent for resource

    - headers, body, and file are the class attribute for resource requests

    - requests are the class property for get the requests from resources that has been called

    - validation are the function to validate the requests for resource
    """

    headers, body, file = [{}, {}, {}]

    @property
    def requests(self) -> dict:
        """
        Property class function for get and filter the requests from requests

        :@return dict: Requests results as dictionary
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

        return _req.to_dict(flat=True)

    def validation(self, csrf_enable=True, **kwargs) -> dict:
        """
        This function will validate your requests resource
        @param csrf_enable:
        @param kwargs:
        @return:
        """
        try:
            dict_validation = {}

            for k, v in kwargs.items():
                validate = v.split(',')
                tmp_validators = []

                if 'required' in validate:
                    tmp_validators.append(DataRequired())

                if 'numeric' in validate:
                    dict_validation[k] = IntegerField(k, validators=tmp_validators)
                else:
                    dict_validation[k] = StringField(k, validators=tmp_validators)
        except KeyError as err:
            raise KeyError.with_traceback(err.__traceback__)
        else:
            class_name = f'{self.__class__.__name__.lower()}_forms_validation'
            if not csrf_enable:
                validate = type(class_name, (FlaskForm,), dict_validation)(csrf_enabled=False)
            else:
                validate = type(class_name, (FlaskForm,), dict_validation)()

            if not validate.validate():
                return {
                    'errors': validate.errors,
                    'code': 422
                }
            else:
                return {
                    'errors': None
                }
