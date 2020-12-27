from abc import ABC

# flask module required
from flask import request, session
from flask_wtf import FlaskForm

# wtforms module required
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError

from metric.app.view import View


class Resource(ABC, View):
    """
    Base class resource, used as parent for resource

    - headers, body, and file are the class attribute for resource requests

    - requests are the class property for get the requests from resources that has been called

    - validation are the function to validate the requests for resource
    """

    headers, body, file = [{}, {}, {}]

    def __init__(self):
        """
        class resource
        """
        super(Resource, self).__init__()
        class_name = f'{self.__class__.__name__.lower()}_forms_validation'
        self.forms = type(class_name, (FlaskForm,), {})

    @property
    def requests(self) -> dict:
        """
        Property class function for get and filter the requests from requests

        :@return _req.to_dict: Requests results as dictionary
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
                    tmp_validators.append(DataRequired(f'field {k} is required'))
                if 'email' in validate:
                    tmp_validators.append(Email(f'field {k} is required and valid email type'))

                # defining field-type
                if 'numeric' in validate:
                    dict_validation[k] = IntegerField(k, validators=tmp_validators)
                else:
                    dict_validation[k] = StringField(k, validators=tmp_validators)
        except KeyError as err:
            raise ValidationError.with_traceback(err.__traceback__)
        else:
            class_name = f'{self.__class__.__name__.lower()}_forms_validation'
            if not csrf_enable:
                self.forms = type(class_name, (FlaskForm,), dict_validation)(csrf_enabled=False)
            else:
                self.forms = type(class_name, (FlaskForm,), dict_validation)()

            if not self.forms.validate():
                return {
                    'errors': self.forms.errors,
                    'code': 422
                }
            else:
                return {
                    'errors': None
                }
