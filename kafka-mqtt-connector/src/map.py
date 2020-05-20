FORWARD_MAP = {
    'device-0001': {
        'light1': 'L001/light1',
        'light2': 'L001/light2'
    },
    
    'device-0002': {
        'light1': 'L002/light1',
        'light2': 'L002/light2'
    }
}

BACKWARD_MAP = {
    'L001/light1': {
        'uuid': 'device-0001',
        'action': 'light1'
    },
    'L001/light2': {
        'uuid': 'device-0001',
        'action': 'light2'
    },
    'L002/light1': {
        'uuid': 'device-0002',
        'action': 'light1'
    },
    'L002/light2': {
        'uuid': 'device-0002',
        'action': 'light2'
    }
}
