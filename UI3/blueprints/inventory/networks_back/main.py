import os
import yaml
import shutil
from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, abort


# Path to file
FILE_SETTINGS = 'inventory/group_vars/all/networks.yml'

# Load YAML
def load_yaml():
    if not os.path.exists(FILE_SETTINGS):
        return {}
    with open(FILE_SETTINGS, 'r') as f:
        return yaml.safe_load(f) or {}

# Save YAML
def save_yaml(data):
    with open(FILE_SETTINGS, 'w') as f:
        yaml.dump(data, f)

# Flask setup
networks_back = Blueprint('networks_back', __name__)
api = Api(networks_back)

class NetworksListResource(Resource):

    def get(self):
        networks = load_yaml()
        if not 'networks' in networks:
            return {}
        return networks['networks'], 200

    def post(self):
        new_networks = request.get_json(force=True)
        save_yaml({'networks': new_networks})
        return {'message': 'Networks written'}, 201

    def put(self):
        new_networks = request.get_json(force=True)
        old_networks = load_yaml()
        old_networks['networks'].update(new_networks)
        save_yaml(old_networks)
        return {'message': 'Networks updated'}, 200

class NetworksResource(Resource):

    def get(self, network):
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        network = networks['networks'][network]
        return network, 200

    def put(self, network):
        updated_network = request.get_json(force=True)
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        networks['networks'][network].update(updated_network)
        save_yaml(networks)
        return {'message': 'Network updated', 'network': updated_network}, 200

    def post(self, network):
        new_setting = request.get_json(force=True)
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        networks['networks'][network][new_setting['setting']] = new_setting['value']
        save_yaml(networks)
        return {'message': 'New network setting written', 'network': network, 'setting': new_setting['value']}, 201

    def delete(self, network):
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        del networks['networks'][network]
        save_yaml(networks)
        return {'message': 'Network deleted', 'network': network}, 200


class NetworksSettingsResource(Resource):

    def get(self, network, setting):
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        if not setting in networks['networks'][network]:
            abort(404, message="Setting not found")
        setting = networks['networks'][network][setting]
        return setting, 200

    def put(self, network, setting):
        new_setting_value = request.get_json(force=True)
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        if not setting in networks['networks'][network]:
            abort(404, message="Setting not found")
        networks['networks'][network][setting] = new_setting_value['value']
        save_yaml(networks)
        return {'message': 'Network setting updated', 'network': new_network, 'setting': new_setting['value']}, 200

    def delete(self, network, setting):
        networks = load_yaml()
        if not network in networks['networks']:
            abort(404, message="Network not found")
        if not setting in networks['networks'][network]:
            abort(404, message="Setting not found")
        del networks['networks'][network][setting]
        save_yaml(networks)
        return {'message': 'Setting deleted', 'network': network, 'setting': setting}, 200

# Routes
api.add_resource(NetworksListResource, '/api/v1/inventory/networks')
api.add_resource(NetworksResource, '/api/v1/inventory/networks/<string:network>')
api.add_resource(NetworksSettingsResource, '/api/v1/inventory/networks/<string:network>/<string:setting>')
