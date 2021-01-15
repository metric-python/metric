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
        ____Base class for resources, read the documentation for more information about the resources____
        """
        super(Resource, self).__init__()

        # ____building form class for resources validation____
        self._class_name = self.__class__.__name__

    @property
    def requests(self):
        """
        ____An property class for extract the requests from resources____

        @return: Requests results as dictionary
        """
        _requests = lambda: None

        if request.json is not None:
            _requests.json = request.json

        if bool(request.form):
            _requests.form = request.form.to_dict(flat=False)

            if bool(request.files):
                _requests.file = request.files.to_dict(flat=False)

        if bool(request.args):
            _requests.args = request.args

        return _requests

    def validation(self, csrf_enable=True, **kwargs):
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
            forms = type(f'{self._class_name.lower()}_forms_validation', (FlaskForm,), dict_validation)
            forms = forms(csrf_enabled=False) if not csrf_enable else forms()

            if not forms.validate():
                return {'errors': forms.errors, 'code': 422}
            else:
                return {'code': 200}
