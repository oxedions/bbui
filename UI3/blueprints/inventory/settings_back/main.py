import os
import yaml
import shutil
from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, abort


# Path to file
FILE_SETTINGS = 'inventory/group_vars/all/settings.yml'

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
settings_back = Blueprint('settings_back', __name__)
api = Api(settings_back)

class SettingsListResource(Resource):

    def get(self):
        settings_parameters = load_yaml()
        return settings_parameters, 200

    def post(self):
        new_settings = request.get_json(force=True)
        save_yaml(new_settings)
        return {'message': 'Settings settings written'}, 201

    def put(self):
        new_settings = request.get_json(force=True)
        old_settings = load_yaml()
        save_yaml(old_settings.update(new_settings))
        return {'message': 'Settings settings updated'}, 200

class SettingsResource(Resource):

    def get(self, setting):
        settings_parameters = load_yaml()
        if not setting in settings_parameters:
            abort(404, message="Setting not found")
        setting = settings_parameters[setting]
        return setting, 200

    def put(self, setting):
        new_setting = request.get_json(force=True)
        settings_parameters = load_yaml()
        if not setting in settings_parameters:
            abort(404, message="Setting not found")
        settings_parameters[setting] = new_setting['value']
        save_yaml(settings_parameters)
        return {'message': 'Setting updated', 'setting': new_setting['value']}, 200

    def delete(self, setting):
        settings_parameters = load_yaml()
        if not setting in settings_parameters:
            abort(404, message="Setting not found")
        del settings_parameters[setting]
        save_yaml(settings_parameters)
        return {'message': 'Setting deleted', 'setting': setting}, 200


# Routes
api.add_resource(SettingsListResource, '/api/v1/inventory/settings')
api.add_resource(SettingsResource, '/api/v1/inventory/settings/<string:setting>')
