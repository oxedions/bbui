import os
import yaml
from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, abort

# Path to YAML DB
YAML_NODES_DB = 'inventory/cluster/nodes.yml'
INI_NODES_GROUPS = 'inventory/cluster/groups'


# Load YAML
def load_yaml():
    if not os.path.exists(YAML_NODES_DB):
        return {}
    with open(YAML_NODES_DB, 'r') as f:
        return yaml.safe_load(f)['all']['children'] or {}

# Save YAML
def save_yaml(data):
    with open(YAML_NODES_DB, 'w') as f:
        yaml.dump({'all':{'children':data}}, f)

def write_INI(data: dict, filename: str):
    """Write dictionary to a custom file format with [key] headers and list values line by line. (INI like)"""
    with open(filename, 'w') as file:
        for key, values in data.items():
            file.write(f'[{key}]\n')
            for value in values:
                file.write(f'{value}\n')

def read_INI(filename: str) -> dict:
    """Read a custom formatted file (INI like) into a dictionary."""
    result = {}
    current_key = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('[') and line.endswith(']'):
                current_key = line[1:-1]
                result[current_key] = []
            elif current_key is not None:
                result[current_key].append(line)
            else:
                raise ValueError(f"Value without section header found: {line}")
    
    return result

# Flask setup
nodes = Blueprint('nodes', __name__)
api = Api(nodes)

class NodeListResource(Resource):
    def get(self):
        nodes_list = load_yaml()
        # We need to gather nodes group too
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        for node in nodes_list:
            node_groups = {'fn_group':"", 'os_group':"", 'hw_group':""}
            for group in groups_list_nodes:
                if node in groups_list_nodes[group]:
                    for group_prefix in ['fn_', 'os_', 'hw_']:
                        if group.startswith(group_prefix):
                            node_groups[str(group_prefix + 'group')] = group
            # Add groups to node returned
            nodes_list[node].update(node_groups)
        return nodes_list, 200

    def post(self):
        new_node = request.get_json(force=True)
        nodes_list = load_yaml()
        node_name = new_node.pop('name')
        if node_name in nodes_list:
            return {'message': 'Node already in the inventory', 'node': node_name}, 409
        if 'fn_group' in new_node or 'hw_group' in new_node or 'os_group' in new_node:
            groups_list_nodes = read_INI(INI_NODES_GROUPS)
            for group_prefix in ['fn_', 'os_', 'hw_']:
                if str(group_prefix + 'group') in new_node:
                    group = new_node.pop(str(group_prefix + 'group'))
                    if group not in groups_list_nodes:
                        return {'message': 'Node group doesnt exist', 'group': group, 'node': node_name}, 404
                    groups_list_nodes[group].append(node_name)
            write_INI(groups_list_nodes, INI_NODES_GROUPS)
        nodes_list[node_name] = new_node
        save_yaml(nodes_list)
        return {'message': 'Node added', 'node': node_name}, 201

class NodeResource(Resource):

    def get(self, node_name):
        # Get node from main list with its parameters
        nodes_list = load_yaml()
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        node = nodes_list[node_name]
        # Now check if node belongs to any group
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        node_groups = {'fn_group':"", 'os_group':"", 'hw_group':""}
        for group in groups_list_nodes:
            if node_name in groups_list_nodes[group]:
                for group_prefix in ['fn_', 'os_', 'hw_']:
                    if group.startswith(group_prefix):
                        node_groups[str(group_prefix + 'group')] = group
        # Add groups to node returned
        node.update(node_groups)
        return node, 200

    def put(self, node_name):
        updated_node = request.get_json(force=True)
        if 'name' in updated_node:
            del updated_node['name']
        # Get node from main list with its parameters
        nodes_list = load_yaml()
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        # Check if we need to update groups
        # Remember to check for conflicts, so we purge the node from groups when needed
        if 'fn_group' in updated_node or 'hw_group' in updated_node or 'os_group' in updated_node:
            groups_list_nodes = read_INI(INI_NODES_GROUPS)
            for group_prefix in ['fn_', 'os_', 'hw_']:
                if str(group_prefix + 'group') in updated_node:
                    # Purge first from all groups related
                    for group in groups_list_nodes:
                        if group.startswith(group_prefix) and node_name in groups_list_nodes[group]:
                            groups_list_nodes[group].remove(node_name)
                    # Now add to group
                    groups_list_nodes[updated_node.pop(str(group_prefix + 'group'))].append(node_name)
            write_INI(groups_list_nodes, INI_NODES_GROUPS)
        nodes_list[node_name] = updated_node
        save_yaml(nodes_list)
        return {'message': 'Node updated', 'node': node_name}, 200

    def delete(self, node_name):
        nodes_list = load_yaml()
        if node_name not in nodes_list:
            abort(404, message="Node not found")
        # Check if we need to purge groups
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        for group in groups_list_nodes:
            if node_name in group:
                groups_list_nodes[group].remove(node_name)
        write_INI(groups_list_nodes, INI_NODES_GROUPS)
        # Now delete node from main list and return
        del nodes_list[node_name]
        save_yaml(nodes_list)
        return {'message': 'Node deleted', 'node': node_name}, 200

# Routes
api.add_resource(NodeListResource, '/api/v1/inventory/nodes')
api.add_resource(NodeResource, '/api/v1/inventory/nodes/<string:node_name>')
