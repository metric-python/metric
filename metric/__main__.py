from kommand import control


if __name__ == '__main__':
    control(
        name='Metric',
        version='0.1a1',
        init={
            'exec': 'metric.console.init',
            'help': 'Init a project'
        },
        resource_generate={
            'exec': 'metric.console.generate.resource',
            'help': 'Generate a resource'
        }
    )
