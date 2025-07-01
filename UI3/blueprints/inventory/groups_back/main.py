import os
import yaml
import shutil
from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, abort


# Path to INI files
INI_NODES_GROUPS = 'inventory/cluster/groups'
FOLDER_NODES_GROUPS = 'inventory/group_vars/'

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
groups_back = Blueprint('groups_back', __name__)
api = Api(groups_back)

class GroupsListResource(Resource):
    def get(self):
        groups_list = {}
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        for group_name, group_nodes in groups_list_nodes.items():
            print(group_name)
            print(group_nodes)
            groups_list[group_name] = {}
            groups_list[group_name]['nodes'] = group_nodes
            with open(FOLDER_NODES_GROUPS + group_name + '/settings.yml', 'r') as f:
                group_settings = yaml.safe_load(f) or {}
            print(groups_list)
            print(group_settings)
            groups_list[group_name].update(group_settings)
        return groups_list, 200

    def post(self):
        new_group = request.get_json(force=True)
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        group_name = new_group.pop('name')
        if group_name in groups_list_nodes:
            return {'message': 'Group already exist', 'group': group_name}, 409
        if 'nodes' in new_group:
            groups_list_nodes[group_name] = new_group.pop('nodes')
        else:
            groups_list_nodes[group_name] = []
        write_INI(groups_list_nodes, INI_NODES_GROUPS)
        os.makedirs(FOLDER_NODES_GROUPS + group_name)
        with open(FOLDER_NODES_GROUPS + group_name + '/settings.yml', 'w') as f:
            yaml.dump(new_group, f)
        return {'message': 'Group added', 'group': group_name}, 201

class GroupResource(Resource):

    # def post(self, group_name):
    #     groups_list = read_INI(INI_NODES_GROUPS)
    #     if group_name not in groups_list:
    #         abort(404, message="Group not found")
    #     new_member = request.get_json(force=True)
    #     node_name = new_member['name']
    #     if node_name in groups_list[group_name]:
    #         return {'message': 'Node already exist in the group', 'node': node_name}, 409
    #     groups_list[group_name].append(node_name)
    #     write_INI(groups_list, INI_NODES_GROUPS)
    #     return {'message': 'Node added to group', 'group': group_name, 'node': node_name}, 201

    def get(self, group_name):
        # Read INI for list of nodes
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        group = {}
        if group_name not in groups_list_nodes:
            abort(404, message="Group not found")
        group['nodes'] = groups_list_nodes[group_name]
        # Gather group settings
        with open(FOLDER_NODES_GROUPS + group_name + '/settings.yml', 'r') as f:
            group_settings = yaml.safe_load(f) or {}
        group.update(group_settings)
        return group, 200

    def put(self, group_name):
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        if group_name not in groups_list_nodes:
            abort(404, message="Group not found")
        updated_group = request.get_json(force=True)
        # Update nodes if relevant
        if 'nodes' in updated_group:
            groups_list_nodes[group_name] = updated_group.pop('nodes')
            write_INI(groups_list_nodes, INI_NODES_GROUPS)
        if len(updated_group) > 0: # Means there are additional parameters, update and write them
            with open(FOLDER_NODES_GROUPS + group_name + '/settings.yml', 'r') as f:
                    group = yaml.safe_load(f) or {}
            group.update(updated_group)
            with open(FOLDER_NODES_GROUPS + group_name + '/settings.yml', 'w') as f:
                yaml.dump(group, f)
        return {'message': 'Group updated', 'group': group_name}, 200

    def delete(self, group_name):
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        if group_name not in groups_list_nodes:
            abort(404, message="Group not found")
        del groups_list_nodes[group_name]
        write_INI(groups_list_nodes, INI_NODES_GROUPS)
        shutil.rmtree(FOLDER_NODES_GROUPS + group_name)
        return {'message': 'Group deleted', 'group': group_name}, 200

class GroupNodeListResource(Resource):

    def get(self, group_name):
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        if group_name not in groups_list_nodes:
            abort(404, message="group not found")
        return groups_list_nodes[group_name], 200

    def post(self, group_name):
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        if group_name not in groups_list_nodes:
            abort(404, message="group not found")
        new_node = request.get_json(force=True)
        node_name = new_node.pop('name')
        if node_name in groups_list_nodes[group_name]:
            return {'message': 'Node already in group', 'group': group_name, 'node': node_name}, 409
        groups_list_nodes[group_name].append(node_name)
        write_INI(groups_list_nodes, INI_NODES_GROUPS)
        return {'message': 'Node added to group', 'group': group_name, 'node': node_name}, 200

class GroupNodeResource(Resource):

    def delete(self, group_name, node_name):
        groups_list_nodes = read_INI(INI_NODES_GROUPS)
        if group_name not in groups_list_nodes:
            abort(404, message="group not found")
        if node_name not in groups_list_nodes[group_name]:
            abort(404, message="Node not found")
        groups_list_nodes[group_name].remove(node_name)
        write_INI(groups_list_nodes, INI_NODES_GROUPS)
        return {'message': 'Node removed from group', 'group': group_name, 'node': node_name}, 200


# Routes
api.add_resource(GroupsListResource, '/api/v1/inventory/groups')
api.add_resource(GroupResource, '/api/v1/inventory/groups/<string:group_name>')
api.add_resource(GroupNodeListResource, '/api/v1/inventory/groups/<string:group_name>/nodes')
api.add_resource(GroupNodeResource, '/api/v1/inventory/groups/<string:group_name>/nodes/<string:node_name>')
