"""
** #VIEW **
---
[ID]
    View adalah class based yang di gunakan untuk templating layout pada framework dan render template tersebut
    menjadi sebuah tampilan html.
[EN]
    View is a class based that is used to templating the layout to the framework and rendering it into HTML display.

:version 1.0.1
"""
import os
from abc import ABCMeta

from jinja2 import Environment
from jinja2 import FileSystemLoader

from metric.src import APPPATH


class ViewFileException(Exception):
    def __init__(self, exception, message="View need valid file!"):
        """
        ## ViewFIleException (Exception class)

        [ID]
            Exception class untuk mendefinisikan bahwa file yang di attach ke dalam View tidak value/error.
        [EN]
            Exception class used to define the file that attached inside the View is invalid/error.

        :param exception: the exception error message
        :param message: message for the error description of this exception
        """
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.exception}'


class View(metaclass=ABCMeta):
    view_file = None

    def __init__(self, extension='html'):
        """
        ## View (Abstract base class)

        [ID]
            View adalah class untuk melakukan templating pada frmaework metric, class ini perlu di pasang sebagai parent
            dari class lain untuk menjalankannya.
        [EN]
            View is a class used as metric framework template engine, this class need to attach as the parent class on
            your other class in order to run it.

        :param extension: define the type of the file extension
        """
        self.env = Environment(
            loader=FileSystemLoader(searchpath=os.path.join(APPPATH, 'views'))
        )
        self.extension = extension

    def render(self, view_file=None, **kwargs):
        """
        ## render (class method)

        :param kwargs: the render options written in dict
        :return: render object
        """
        if view_file is not None:
            view_file = view_file.split('.')
            view_file[-1] = f'{view_file[-1]}.{self.extension}'
        else:
            raise ViewFileException('No file to be define')

        loader = self.env.get_template(os.path.join(*view_file))
        return loader.render(**kwargs)
