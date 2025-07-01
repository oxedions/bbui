import os
import yaml
from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, abort

# Path to YAML DB
YAML_NODES_DB = 'inventory/cluster/nodes.yml'

# Load YAML DB
def load_db():
    if not os.path.exists(YAML_NODES_DB):
        return {}
    with open(YAML_NODES_DB, 'r') as f:
        return yaml.safe_load(f)['all']['children'] or {}

# Save YAML DB
def save_db(data):
    with open(YAML_NODES_DB, 'w') as f:
        yaml.dump({'all':{'children':data}}, f)

# Flask setup
nodes = Blueprint('nodes', __name__)
api = Api(nodes)

class NodeListResource(Resource):
    def get(self):
        nodes_list = load_db()
        return nodes_list, 200

    def post(self):
        new_node = request.get_json(force=True)
        nodes_list = load_db()
        node_name = new_node['name']
        del new_node['name']
        nodes_list[node_name]=new_node
        save_db(nodes_list)
        return {'message': 'Node added', 'node': node_name}, 201

class NodeResource(Resource):

    def get(self, node_name):
        nodes_list = load_db()
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        return nodes_list[node_name], 200

    def put(self, node_name):
        updated_node = request.get_json(force=True)
        nodes_list = load_db()
        if 'name' in updated_node:
            del updated_node['name']
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        nodes_list[node_name] = updated_node
        save_db(nodes_list)
        return {'message': 'Node updated', 'node': node_name}, 200

    def delete(self, node_name):
        nodes_list = load_db()
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        del nodes_list[node_name]
        save_db(nodes_list)
        return {'message': 'Node deleted', 'node': node_name}, 200

# Routes
api.add_resource(NodeListResource, '/api/v1/inventory/nodes')
api.add_resource(NodeResource, '/api/v1/inventory/nodes/<string:node_name>')
