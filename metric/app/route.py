from inspect import isclass

from metric.src import Base


class Route(Base):
    def __init__(self):
        super(Route, self).__init__()

    def route(self, resource, **kwargs):
        if all(k in kwargs for k in ['url', 'method', 'endpoint']):
            url, method, endpoint = kwargs['url'], kwargs['method'], kwargs['endpoint']

            if not isinstance(kwargs['method'], list):
                kwargs['method'] = list(kwargs['method'])
            return self.app.route(url, method=method, endpoint=endpoint)(resource)

    def resource(self, cls, prefix='/'):
        if isclass(cls):
            list_resource = ['get', 'post', 'put', 'delete']
            resource = [i for i in dir(cls) if i in list_resource]

            for i in resource:
                endpoint = '.'.join([cls.__name__.lower(), i])
                base_url = '/'.join([prefix, cls.__name__.lower()])

                url = f'{base_url}/<int:id>' if i in ['delete', 'put'] else base_url
                self.route(getattr(cls(), i), method=i.upper(), endpoint=endpoint, url=url)
