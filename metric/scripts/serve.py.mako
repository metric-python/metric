"""
Main serve class for your application, read the docs for more information :)
:version ${version}
"""

from metric import Metric


class Serve(Metric):
    def __init__(self):
        super(Serve, self).__init__()

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    # remove the comment line below for automatic gathering-register resource route
    # Serve.resource()
    Serve().run()
