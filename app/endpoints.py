from flask import jsonify, request
from . import api
from . import disks
from .decorators import restricted


@api.route('/<node>/disks/', methods=['GET'])
@api.route('/<node>/disks', methods=['GET'])
def get_disks(node):
    if request.args.get('free') is not None:
        results = disks.get_free(node)
    elif request.args.get('used') is not None:
        results = disks.get_used(node)
    else:
        results = disks.get(node)
    return jsonify(results)


@api.route('/<node>/disks/<disk>', methods=['GET'])
def get_disk_info(node, disk):
    return jsonify({disk: disks.get(node)[disk]})


@api.route('/<node>/disks/<disk>', methods=['PUT'])
def update_disk_status(node, disk):
    # Handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        disk_status = data['status']
        disk_clustername = data['clustername']
        disk_node = data['node']
    # Handle form param requests: eg. curl -d status=free
    else:
        disk_status = request.form.get('status')
        disk_clustername = request.form.get('clustername')
        disk_node = request.form.get('node')
    if disk_status is not None:
        disks.set_status(node, disk, disk_status, disk_clustername, disk_node)
        return '', 204
    else:
        return jsonify({'status': '400',
                        'error': 'Invalid request',
                        'message': 'Unable to get the new '
                                   'node status from the request'}), 400


@api.route('/test', methods=['GET'])
@restricted(role='ROLE_USER')
def echo_hello():
    return jsonify({'message': 'Hello'})
