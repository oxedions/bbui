import os
import re
import yaml
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from functions import load_yaml,dump_yaml,mergearrays
import requests
import shutil


master_groups = Blueprint('master_groups', __name__, template_folder='templates')

etc_path = 'C:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))
polarbear_parameters = load_yaml(os.path.join(etc_path,'parameters.yml'))

####################################################################################################
##################################### /inventory/master_groups #####################################

################## GET

@master_groups.route("/inventory/master_groups/index.html", methods = ['GET'])
def inventory_master_groups_get():

    flags={'status': None}
    # Grab status if it was passed as arguments
    if 'status' in request.args:
        if request.args['status'] == "updated":
            flags['status'] = "updated"
        if request.args['status'] == "error":
            flags['status'] = "error"
    
    # Request list of master groups and their data
    mg_data = get_existing_master_groups()
    master_groups_data = {}
    for mg, mg_values in mg_data.items():
        new_mg = mg.replace("mg_","")
        master_groups_data[new_mg] = {}
        master_groups_data[new_mg].update(mg_values)

    return render_template("page.html.j2", \
                            page_content_path="master_groups/index.html.j2", \
                            page_title="Inventory - Master Groups", \
                            page_navigation_data=page_navigation_data, \
                            page_left_menu="master_groups/menu.html.j2", \
                            left_menu_active="index", \
                            master_groups_data=master_groups_data)

@master_groups.route("/v1/inventory/master_groups", methods = ['GET'])
def inventory_master_groups_get_api():
    return jsonify(get_existing_master_groups()), 200

####################################################################################################
##################################### /inventory/master_groups/add #################################

################## GET

@master_groups.route("/inventory/master_groups/add.html", methods = ['GET'])
def inventory_master_groups_add_get():

    return render_template("page.html.j2", \
                            page_content_path="master_groups/add.html.j2", \
                            page_title="Inventory - Master Groups - Add", \
                            page_navigation_data=page_navigation_data, \
                            page_left_menu="master_groups/menu.html.j2", \
                            left_menu_active="add")

################## POST

@master_groups.route("/inventory/master_groups/add.html", methods = ['POST'])
def inventory_master_groups_add_post():
    mg_data = mergearrays(request.form)
    mg_data['master_group_name'] = "mg_" + mg_data['master_group_name']
    create_new_master_groups(mg_data)
    return redirect(url_for("master_groups.inventory_master_groups_get", status="updated"))

@master_groups.route("/v1/inventory/master_groups/add", methods=['POST'])
def inventory_master_groups_add_post_api(): # Add or update a master_group
    create_new_master_groups(mergearrays(request.form))
    return "OK", 200

####################################################################################################
##################################### /inventory/master_groups/manage ##############################

################## GET

@master_groups.route("/inventory/master_groups/manage.html", methods = ['GET'])
def inventory_master_groups_manage_get():

    master_group = request.args.get('master_group')
    master_group_data = get_master_group_data("mg_" + master_group)
    master_group_data['master_group_variables'] = yaml.dump(master_group_data['master_group_variables'])

    return render_template("page.html.j2", \
                            page_content_path="master_groups/manage.html.j2", \
                            page_title="Inventory - Master Groups - Manage", \
                            page_navigation_data=page_navigation_data, \
                            page_left_menu="master_groups/menu.html.j2", \
                            left_menu_active="manage", \
                            master_group_data=master_group_data, \
                            master_group=request.args.get('master_group'))

################## POST

@master_groups.route("/inventory/master_groups/manage.html", methods = ['POST'])
def inventory_master_groups_manage_post():
    mg_data = mergearrays(request.form)
    mg_data['master_group_name'] = "mg_" + mg_data['master_group_name']
    create_new_master_groups(mg_data)
    return redirect(url_for("master_groups.inventory_master_groups_get", status="updated"))

####################################################################################################
##################################### /inventory/master_groups/delete #################################

################## GET

@master_groups.route("/inventory/master_groups/delete.html", methods = ['GET'])
def inventory_master_groups_delete_get():

    # Request list of master groups and their data
    mg_data = get_existing_master_groups()
    master_groups_data = {}
    for mg, mg_values in mg_data.items():
        new_mg = mg.replace("mg_","")
        master_groups_data[new_mg] = {}
        master_groups_data[new_mg].update(mg_values)

    return render_template("page.html.j2", \
                            page_content_path="master_groups/delete.html.j2", \
                            page_title="Inventory - Master Groups - Add", \
                            page_navigation_data=page_navigation_data, \
                            page_left_menu="master_groups/menu.html.j2", \
                            left_menu_active="delete", \
                            master_groups_data=master_groups_data)

@master_groups.route("/inventory/master_groups/delete.html", methods = ['POST'])
def inventory_master_groups_delete_post():
    mg_data = mergearrays(request.form)
    mg_data['master_group_name'] = "mg_" + mg_data['master_group_name']
    delete_master_group(mg_data['master_group_name'])
    return redirect(url_for("master_groups.inventory_master_groups_get", status="updated"))

##########################################################################################
########################################################################################
######################################################################################
################## FUNCTIONS
################
##############


def get_existing_master_groups():

    # Gather list of existing groups that matches mg_
    master_groups_data = {}
    for folder in os.listdir(os.path.join(polarbear_parameters['inventory_path'],"group_vars")):
        if re.match('^mg_.*', folder):
             yaml_buffer = load_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",folder,"data.yml"))
             master_groups_data[folder] = yaml_buffer
    return master_groups_data


def get_master_group_data(master_group):

    master_group_data = load_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",master_group,"data.yml"))
    master_group_data_variables = load_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",master_group,"variables.yml"))
    if str(master_group_data_variables) == 'None':
        master_group_data['master_group_variables'] = ''
    else:
        master_group_data['master_group_variables'] = {}
        master_group_data['master_group_variables'].update(master_group_data_variables)

    return master_group_data


def create_new_master_groups(mg_data): # Add or update a master_group
    # Check if folder already exist
    folder_exist = os.path.exists(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg_data['master_group_name']))
    if not folder_exist:
        os.makedirs(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg_data['master_group_name']))
        os.close(os.open(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg_data['master_group_name'],"variables.yml"), os.O_CREAT))
    # Manage variables if exist
    if "master_group_variables" in mg_data:
        dump_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg_data['master_group_name'],"variables.yml"), yaml.safe_load(mg_data['master_group_variables']))
        mg_data.pop('master_group_variables')
    # Add data
    dump_yaml(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg_data['master_group_name'],"data.yml"),mg_data)


def delete_master_group(mg): # Delete a master group
    shutil.rmtree(os.path.join(polarbear_parameters['inventory_path'],"group_vars",mg))
