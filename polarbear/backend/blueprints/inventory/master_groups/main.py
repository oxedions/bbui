import os
import re
import yaml
from flask import Blueprint, render_template, request,jsonify
from functions import load_yaml,dump_yaml

master_groups = Blueprint('master_groups', __name__, template_folder='templates')

etc_path = 'I:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))
polarbear_parameters = load_yaml(os.path.join(etc_path,'parameters.yml'))

@master_groups.route("/v1/inventory/master_groups", methods = ['GET'])
def inventory_master_groups_index():

    # Gather list of existing groups that are not all or equipment_ or mg_
    master_groups_data = {}
    for folder in os.listdir(os.path.join(polarbear_parameters['inventory_path'],"group_vars")):
        if re.match('^mg_.*', folder):
             yaml_buffer = load_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",folder,"data.yml"))
             master_groups_data[folder] = yaml_buffer
    return jsonify(master_groups_data), 200

@master_groups.route("/v1/inventory/master_groups", methods=['POST'])
def master_groups_post(): # Add or update a master_group

    # Check if folder already exist
    folder_exist = os.path.exists(os.path.join(polarbear_parameters['inventory_path'],"group_vars",request.get_json()['master_group_name']))
    if not folder_exist:
        os.makedirs(os.path.join(polarbear_parameters['inventory_path'],"group_vars",request.get_json()['master_group_name']))
        os.close(os.open(os.path.join(polarbear_parameters['inventory_path'],"group_vars",request.get_json()['master_group_name'],"variables.yml"), os.O_CREAT))
    # Add data
    dump_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",request.get_json()['master_group_name'],"data.yml"),{'description':request.get_json()['master_group_description']})
    # Manage variables if exist
    if "master_group_variables" in request.get_json():
        dump_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",request.get_json()['master_group_name'],"data.yml"),request.get_json()['master_group_variables'])

    return "OK", 200
