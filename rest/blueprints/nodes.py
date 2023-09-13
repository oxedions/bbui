import os
import re
import yaml
from flask import Blueprint, render_template, request,jsonify
from flask_restful import Api, Resource, url_for

nodes = Blueprint('nodes', __name__)
api = Api(nodes)

# Define the path to the YAML file
yaml_file_path = 'inventory/cluster/nodes.yml'



#################### GLOBAL FUNCTIONS ####################
# Load nodes data from the YAML file
def load_nodes_from_file():
    if os.path.exists(yaml_file_path):
        with open(yaml_file_path, 'r') as file:
            nodes = yaml.safe_load(file)['all']['hosts']
            return nodes
    else:
        return {}

# Save nodes data to the YAML file
def save_nodes_to_file(nodes):
    with open(yaml_file_path, 'w') as file:
        all_nodes = {'all': {'hosts': {}}}
        all_nodes['all']['hosts'] = nodes
        yaml.dump(all_nodes, file, default_flow_style=False)



#################### ROOT CALL /nodes ####################

def nodes_get():
    nodes = load_nodes_from_file()
    if nodes is None:
        return {'error': 'No nodes found'}, 400
    nodes_list = []
    for k, v in nodes.items():
        nodes_list.append(k)
    return nodes_list, 200
# HTTP
class nodes_root(Resource):
    def get(self):
        return nodes_get()
api.add_resource(nodes_root, '/nodes')
# CLI calls
def cli_nodes_get(data):
    return nodes_get()



#################### RESOURCES CALL /nodes/<string:node_id> ####################

def nodes_resource_get(node_id):
    nodes = load_nodes_from_file()
    if nodes is None:
        return {'error': 'No nodes found'}, 400
    if node_id not in nodes:
        return {'error': 'Node ' + node_id + 'not found'}, 400
    return nodes[node_id], 200

def nodes_resource_post(data, node_id):
    if node_id is None:
        return {'error': 'Missing node_id'}, 400
    nodes = load_nodes_from_file()
    if node_id in nodes:
        return {'error': 'Node already exists'}, 409
    nodes[node_id] = {
        'network_interfaces': [],
        'bmc': {
            'ip4': '',
            'name': '',
            'mac': ''
        }
    }
    nodes[node_id].update(data, node_id)
    save_nodes_to_file(nodes)
    return {'message': 'Node added successfully'}, 201

def nodes_resource_delete(data, node_id):
    if node_id is None:
        return {'error': 'Missing node_id'}, 400
    nodes = load_nodes_from_file()
    if not node_id in nodes:
        return {'error': 'Node does not exists'}, 409
    del nodes[node_id]
    save_nodes_to_file(nodes)
    return {'message': 'Node deleted successfully'}, 201

# HTTP
class nodes_resource(Resource):
    def get(self, node_id):
        return nodes_resource_get(node_id)
    def post(self, node_id):
        return nodes_resource_post(request.json, node_id)
    def delete(self, node_id):
        return nodes_resource_delete(request.json, node_id)
api.add_resource(nodes_resource, '/nodes/<string:node_id>')


# CLI calls
def cli_nodes_resource_get(data):
    return nodes_resource_get()
def cli_nodes_resource_post(data):
    return nodes_resource_post(data)
def cli_nodes_resource_delete(data):
    return nodes_resource_delete(data)
