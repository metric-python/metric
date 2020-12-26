from metric import Metric
from metric.app.public import Public
from metric.app.routes import route, show_route


class Serve(Metric):
    """
    This class purposely to serve application Metric Framework
    """

    def __init__(self):
        super(Serve, self).__init__()

        # Uncomment the function declared below to auto gather and routing resource
        # self.resource()
        self.route()

    def route(self):
        """
        Public function for showing resource route public directory such as js or css
        """
        route(Public().home, method='GET', endpoint='home', url='/')
        route(Public().getCss, method='GET', endpoint='public.css', url='/css/<path_file>')
        route(Public().getJs, method='GET', endpoint='public.js', url='/js/<path_file>')
        route(Public().getFont, method='GET', endpoint='public.font', url='/font/<path_file>')
        route(Public().getImg, method='GET', endpoint='public.img', url='/img/<path_file>')

    def run(self):
        # change debug to false to disable debug and verbose mode
        self.app.run(
            debug=True,
            port=5000
        )


if __name__ == '__main__':
    Serve().run()
