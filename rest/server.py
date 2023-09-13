from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os
import yaml

app = Flask(__name__)
api = Api(app)

# Define the path to the YAML file
yaml_file_path = 'inventory/cluster/nodes.yml'

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

# Nodes
# shows a list of all nodes, and lets you POST to add new node
class node_resource(Resource):
    def get(self):
        nodes = load_nodes_from_file()
        if nodes is None:
            return {'error': 'No nodes found'}
        return nodes, 200

    def post(self):
        print(request)
        data = request.json
        print(data)
        node_id = data.get('node_id')
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
        save_nodes_to_file(nodes)
        return {'message': 'Node created successfully'}, 201



api.add_resource(node_resource, '/node')

#api.add_resource(node_resource, '/nodes/<string:node_id>')

if __name__ == '__main__':
    app.run(debug=True)