import os
import re
import yaml
from flask import Blueprint, render_template, request,jsonify
from functions import load_yaml,dump_yaml

master_groups = Blueprint('master_groups', __name__, template_folder='templates')

etc_path = 'B:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))
polarbear_parameters = load_yaml(os.path.join(etc_path,'parameters.yml'))

@master_groups.route("/v1/inventory/master_groups", methods = ['GET'])
def inventory_master_groups_index():

    # Gather list of existing groups that are not all or equipment_ or mg_
    master_groups_data = {}
    for folder in os.listdir(polarbear_parameters['inventory_path'] + "/group_vars/"):
        if re.match('^mg_.*', folder):
             yaml_buffer = load_yaml(polarbear_parameters['inventory_path'] + "/group_vars/" + folder + "/data.yml")
             master_groups_data[folder] = yaml_buffer

    return jsonify(master_groups_data), 200
