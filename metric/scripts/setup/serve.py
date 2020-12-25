from metric import Metric


class Serve(Metric):
    """
    This class purposely to serve application Metric Framework
    """

    def __init__(self):
        super(Serve, self).__init__()

        # Uncomment the function declared below to auto gather and routing resource
        # self.resource()

    def run(self):
        # change debug to false to disable debug and verbose mode
        self.app.run(debug=True)


if __name__ == '__main__':
    Serve().run()
