import yaml


def read_yaml(file):
    try:
        with open(file, 'r') as f:
            return yaml.load(f)

    except yaml.YAMLError:
        print('File {} is invalid!'.format(file))
    except FileNotFoundError:
        print('File {} not found!'.format(file))
    except:
        print('Sorry, an unexpected error occured')

    return False