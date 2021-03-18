"""
** #RESOURCE **
---
[ID]
    Resource adalah gerbang pelabuhan yang mengatur jalannya pacakges dari requests dan mengirimkannya kembali dengan
    response.
[EN]
    Resource is a port gate to that regulates the passage of packages by requests and send it back with response.

:version 1.0.1
"""

from abc import ABC
from functools import wraps

from flask import jsonify as _json
from flask import redirect as _rdr
from flask import request as _req
from flask_jwt_extended import jwt_required
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email

from metric.app.view import View


class RequestValidationException(Exception):
    def __init__(self, exception, message="Invalid requests parse!"):
        """
        ## RequestValidationException (Exception class)

        [ID]
            Exception class untuk mendefinisikan bahwa request tidak bisa di parsing karena suatu kesalahan.
        [EN]
            Exception class used to define the request cannot be parsed because error/invalid.

        :param exception: the exception error message
        :param message: message for the error description of this exception
        """
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.exception}'


class Requests:
    parse = lambda: None

    def __init__(self, class_name):
        """
        ## Requests

        [ID]
            Class ini berguna untuk melakukan parsing dan validasi terhadap requests yang masuk.
        [EN]
            This class is used to parsed and validation for incoming requests.
        """
        self.class_name = class_name.lower()

        try:
            if _req.json is not None:
                self.parse.json = _req.json

            if bool(_req.form):
                self.parse.form = _req.form.to_dict(flat=False)

                if bool(_req.files):
                    self.parse.file = _req.files.to_dict(flat=False)

            if bool(_req.args):
                self.parse.args = _req.args
        except AttributeError:
            pass

    def validation(self, csrf_enable=True, **kwargs):
        """
        ## validation

        :param csrf_enable:
        :param kwargs:
        :return:
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
            raise RequestValidationException.with_traceback(err.__traceback__)

        else:
            forms = type(f'{self.class_name}_forms_validation', (FlaskForm,), dict_validation)
            forms = forms(csrf_enabled=False) if not csrf_enable else forms()

            if not forms.validate():
                return {'errors': forms.errors, 'code': 422}
            else:
                return {'code': 200}


class Response:
    def __init__(self):
        """
        ## Response

        [ID]
            Class ini bertujuan untuk memberikan response kepada client, baik itu redirect, json atau HTML.
        [EN]
            This class is purposed to give response to the client which is redirect, json or HTML.
        """
        pass

    def json(self, data, status_code=200):
        return _json(data), status_code

    def redirect(self, target):
        return _rdr(target, 301)


class Resource(ABC, View):
    headers, body = [{}, {}]

    def __init__(self):
        """
        ____Base class for resources, read the documentation for more information about the resources____
        """
        super(Resource, self).__init__()

        # ____building form class for resources validation____
        self.request  = Requests(self.__class__.__name__)
        self.response = Response()

    def tokenRequired(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return jwt_required(wrapper)
