from inspect import isclass

from metric.app import APP
from metric.src.cabin import Cabin

cabin = Cabin()


# ** ROUTE **
def route(func, **kwargs):
    """
    ### ROUTE
    ---
    a basic route function to register resource or function as endpoint manually.
    ---
    """
    try:
        uri = kwargs['url']
        met = kwargs['method']
        endpoint = kwargs['endpoint']

        if not isinstance(met, list):
            met = [met]

        cabin.info(f'register router -> {uri} method -> {met} as endpoint -> {endpoint}')

        return APP.route(uri, methods=met, endpoint=endpoint)(func)
    except KeyError as err:
        pass


# ** RESOURCES **
def resource(cls, prefix='/') -> None:
    """
    ### RESOURCE
    ---
    function used to serve class as resources be route endpoint automatically, and only
    for put or delete endpoint must be attached with parameter id in the resource.
    ---
    """
    if isclass(cls):
        lre = ['get', 'post', 'put', 'delete']
        rsc = [i for i in dir(cls) if i in lre]

        for i in rsc:
            endpoint = '.'.join([cls.__name__.lower(), i])
            base_uri = '/'.join([prefix, cls.__name__.lower()])

            # ____only for "delete and put" resource must be added with id parameter____
            uri = f'{base_uri}/<int:id>' if i in ['delete', 'put'] else base_uri

            route(getattr(cls(), i), method=i.upper(), endpoint=endpoint, url=uri)
