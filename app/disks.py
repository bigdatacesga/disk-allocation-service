"""Disks Allocation API"""
import kvstore

DISKS_VERSION_PATH = "testing"


# Create a global kvstore client
ENDPOINT = 'http://10.112.0.101:8500/v1/kv'
_kv = kvstore.Client(ENDPOINT)
#PREFIX = 'resources/disks'
PREFIX = 'resources/disks/' + DISKS_VERSION_PATH


def get(node):
    """Returns the status of all the disks of a given node"""
    subtree = _kv.recurse('{}/{}'.format(PREFIX, node))
    return _parse_disk_info(subtree)


def get_free(node):
    """Returns the list of free disks of a given node"""
    subtree = _kv.recurse('{}/{}'.format(PREFIX, node))
    freedisks = _filter_disks(subtree, status='free')
    return {'number': len(freedisks), 'disks': freedisks}


def get_used(node):
    """Returns the list of used disks of a given node"""
    subtree = _kv.recurse('{}/{}'.format(PREFIX, node))
    useddisks = _filter_disks(subtree, status='used')
    return {'number': len(useddisks), 'disks': useddisks}


def set_status(node, disk, status, clustername, service_node_name):
    """Sets the status of a given disk"""
    _kv.set('{}/{}/{}/status'.format(PREFIX, node, disk), status)
    _kv.set('{}/{}/{}/clustername'.format(PREFIX, node, disk), clustername)
    _kv.set('{}/{}/{}/node'.format(PREFIX, node, disk), service_node_name)


def _parse_disk_info(subtree):
    disks_info = dict()

    for k in subtree.keys():
        disk_name = _parse_diskname(k)
        disks_info[disk_name] = dict()

    for k in subtree.keys():
        disk_name = _parse_diskname(k)
        disks_info[disk_name][_parse_last_element(k)] = subtree[k]

    return disks_info


def _parse_last_element(key):
    return key.split('/')[-1]


def _parse_diskname(key):
    """Extract disk name from key"""
    return key.split('/')[-2]


def _filter_disks(subtree, status='free'):
    """Filter disks based on status"""
    if status == 'free':
        filtereddisks = [_parse_diskname(k)
                         for k in sorted(subtree.keys())
                         if subtree[k] == 'free' and k.endswith("status")]
    elif status == 'used':
        filtereddisks = [_parse_diskname(k)
                         for k in sorted(subtree.keys())
                         if subtree[k] != 'free' and k.endswith("status")]
    else:
        raise StatusNotSupportedError()

    return filtereddisks


class StatusNotSupportedError(Exception):
    pass

