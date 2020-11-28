from inspect import isclass
from os.path import join
from metric.app import APP


def register_route(func, prefix = ''):
    pass

# ** REGISTER RESOURCES **
def register_resource(cls, prefix = '/') -> None:
    listsres = ['get', 'post', 'put', 'delete']
    resource = [i for i in dir(cls) if i in listsres]

    for i in resource:
        uri = '/'.join([prefix, cls.__name__.lower()])
        resource = getattr(cls(), i)

        if i in ['delete', 'put']:
            uri = f'{uri}/<int:id>'

        endpoint = '.'.join([cls.__name__.lower(), i])
        APP.route(uri, methods=[i.upper()], endpoint=endpoint)(resource)
