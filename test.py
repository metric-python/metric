from metric.app.resource import Resource
from metric.app.routes import register_resource
from metric.app import APP


class Test(Resource):
    def get(self):
        print(self.requests['test'])
        return 'asdf'

if __name__ == '__main__':
    register_resource(Test)

    APP.run(debug=True)