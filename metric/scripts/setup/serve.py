from metric import Metric


class Serve(Metric):
    def __init__(self):
        """
        ____This is class server app, there's some comment-ed code to run some server function____
        """
        super(Serve, self).__init__()

        # self.resource()
        self.admin()

    def run(self):
        # change debug to false to disable debug and verbose mode
        self.app.run(
            debug=True,
            port=5000
        )


if __name__ == '__main__':
    Serve().run()
