import os
from importlib import import_module


def createDirectory(path_dir):
    try:
        os.makedirs(path_dir)
    except FileExistsError as err:
        raise FileExistsError('Directory is already exists!').with_traceback(err.__traceback__)


def createFile(path_file, content = ''):
    try:
        file = open(path_file, 'w')
        file.write(content)
    except OSError as err:
        raise OSError('Cannot write file!').with_traceback(err.__traceback__)
    except FileExistsError as err:
        raise FileExistsError('File is already exists!').with_traceback(err.__traceback__)
    else:
        file.close()


def createPackage(path_dir):
    createDirectory(path_dir)
    createFile(os.path.join(path_dir, '__init__.py'), f'# INIT PACKAGE {path_dir}')


def pathLocation(variable_path, location):
    '''
    ____to get the location file package and the path____
    '''
    if isinstance(location, str):
        location_path = os.path.join(variable_path, location)
        package_name = 'src.%s' % location
        return {'location_path': location_path, 'package_name': package_name}


def auto(dist_path, location, trim):
    '''
    ____crawl into path location to seek and read all files available to import and convert it
    into router raw object dictionary____
    '''
    if isinstance(location, str):
        package_location = pathLocation(dist_path, location)
        loc_path, package_name = package_location['location_path'], package_location['package_name']

        walk_result = []
        for r, d, f in os.walk(loc_path):
            for i in f:
                if '.py' in i and i != '__init__.py' and '.pyc' not in i:
                    name = i[:-3]
                    walk_result.append(os.path.join(r, name))

        crawl_result = []
        for i in walk_result:
            x = os.path.normpath(i).split(os.path.sep)
            pc = ''
            c = 0

            for ix in x[:-1]:
                pc += '%s' % ix.lower()
                c += 1
                if c < len(x) - 1:
                    pc += '.'

            crawl_result.append({'path': pc, 'cls': x[-1]})

        item_result = {}
        for i in crawl_result:
            fp = ''
            for ip in i['path']:
                fp += ip

            path_change = i['path'].replace(trim, '')
            key = path_change + '.' + i['cls']

            # windows issue with path
            item_result[key] = getattr(import_module('.%s' % i['cls'], i['path']), i['cls'].capitalize())

        return item_result
