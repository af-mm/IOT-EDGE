FORWARD_MAP = {
    'device-0001': {
        'light1': {
            'topic': 'mqtt-input',
            'f': """
def f(d):
    if 'a' in d and 'b' in d and 'c' in d:
        return '{},{},{}'.format(d['a'], d['b'], d['c'])
    return None
                """
        },
        'light2': {
            'topic': 'mqtt-input',
            'f': """
def f(d):
    if 'a' in d and 'b' in d and 'c' in d:
        return '{},{},{}'.format(d['c'], d['b'], d['a'])
    return None
                """
        }
    },
    
    'device-0002': {
        'light1': {
            'topic': 'mqtt-input',
            'f': """
def f(d):
    if 'a' in d and 'b' in d and 'c' in d:
        return '{}-{}-{}'.format(d['a'], d['b'], d['c'])
    return None
                """
        },
        'light2': {
            'topic': 'mqtt-input',
            'f': """
def f(d):
    if 'a' in d and 'b' in d and 'c' in d:
        return '{}-{}-{}'.format(d['c'], d['b'], d['a'])
    return None
                """
        }
    }
}

BACKWARD_MAP = {
    'device-0001': {
        'light1': {
            'topic': 'edge-output',
            'f': """
def f(d):
    parts = d.split(',')
    if len(parts) != 3:
        return None
    return {'a': parts[0], 'b': parts[1], 'c': parts[2]}
                """
        },
        'light2': {
            'topic': 'edge-output',
            'f': """
def f(d):
    parts = d.split(',')
    if len(parts) != 3:
        return None
    return {'a': parts[2], 'b': parts[1], 'c': parts[0]}
                """
        }
    },
    
    'device-0002': {
        'light1': {
            'topic': 'edge-output',
            'f': """
def f(d):
    parts = d.split('-')
    if len(parts) != 3:
        return None
    return {'a': parts[0], 'b': parts[1], 'c': parts[2]}
                """
        },
        'light2': {
            'topic': 'edge-output',
            'f': """
def f(d):
    parts = d.split('-')
    if len(parts) != 3:
        return None
    return {'a': parts[2], 'b': parts[1], 'c': parts[1]}
                """
        }
    }
}

def getMapByName(name):
    if name == 'FORWARD_MAP':
        return FORWARD_MAP
    elif name == 'BACKWARD_MAP':
        return BACKWARD_MAP
    
    return {}

