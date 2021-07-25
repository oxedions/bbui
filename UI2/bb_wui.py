import subprocess
from subprocess import Popen, PIPE
import time
from flask import Flask, render_template, request, redirect, jsonify
import re
import os
import yaml
import json

# Colors, from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_yaml(filename):
    print(bcolors.OKBLUE+'[INFO] Loading '+filename+bcolors.ENDC)
    with open(filename, 'r') as f:
        # return yaml.load(f, Loader=yaml.FullLoader) ## Waiting for PyYaml 5.1
        return yaml.load(f)

def save_yaml(filename,yaml_data):
    print(bcolors.OKBLUE+'[INFO] Dumping '+filename+bcolors.ENDC)
    with open(filename, 'w') as f:
        f.write(yaml.dump(yaml_data))
    return 0

app = Flask(__name__)

initialization_form = None

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@app.route("/")
def index():
    return render_template("page.html.j2", page_content_path="content/index.html", page_title="Home")

##### INITIALIZE

@app.route("/initialize/index.html")
def initialize_index():
    return render_template("page.html.j2", page_content_path="content/initialize/index.html", page_title="Initialize")

@app.route("/initialize/step_1.html")
def initialize_step_1():
    print('initialize_step_1')
    return render_template("page.html.j2", page_content_path="content/initialize/step_1.html", page_title="Initialization - Step 1")

@app.route("/initialize/step_2.html", methods = ['POST'])
def initialize_step_2():

    global initialization_form

    if request.method == 'POST':
        initialization_form = {}
        print('initialize_step_2 POST')
        print(request.form)
        initialization_form = request.form.to_dict()
        print('Value' + str(initialization_form))
        return render_template("page.html.j2", page_content_path="content/initialize/step_2.html", page_title="Initialization - Step 2")

@app.route("/initialize/step_3.html", methods = ['POST'])
def initialize_step_3():

    global initialization_form

    if request.method == 'POST':
        print('initialize_step_3 POST')
        print(request.form)
        initialization_form = Merge(initialization_form,request.form.to_dict())
        print('Value' + str(initialization_form))
        return render_template("page.html.j2", page_content_path="content/initialize/step_3.html", page_title="Initialization - Step 3")

@app.route("/initialize/report.html", methods = ['POST'])
def initialize_report():

    global initialization_form

    if request.method == 'POST':
        print('initialize_report POST')
        print(request.form)
        initialization_form = Merge(initialization_form,request.form.to_dict())
        print('Value' + str(initialization_form))
        print('Creating new inventory.')
        print('  - Backup and clean current existing inventory.')
        os.system('mkdir -p /etc/bluebanquise/backups/')
        os.system('tar cvJf /etc/bluebanquise/backups/previous_inventory.tar.xz /etc/bluebanquise/inventory/')
        os.system('rm -Rf /etc/bluebanquise/inventory/')
        print('  - Copy base inventory.')
        os.system('cp -a data/initialize/inventory/ /etc/bluebanquise/')
        print('  - Setting parameters.')
        yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/all/general_settings/general.yml')
        yaml_buffer['cluster_name'] = initialization_form['inventory_cluster_name']
        yaml_buffer['time_zone'] = initialization_form['inventory_time_zone']
        yaml_buffer['icebergs_system'] = initialization_form['inventory_icebergs_system']
        save_yaml('/etc/bluebanquise/inventory/group_vars/all/general_settings/general.yml',yaml_buffer)
        yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/all/general_settings/network.yml')
        yaml_buffer['domain_name'] = initialization_form['inventory_domain_name']
        save_yaml('/etc/bluebanquise/inventory/group_vars/all/general_settings/network.yml',yaml_buffer)
        yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/all/equipment_all/equipment_profile.yml')
        yaml_buffer['ep_operating_system']['distribution'] = initialization_form['ep_operating_system.distribution']
        yaml_buffer['ep_operating_system']['distribution'] = initialization_form['ep_operating_system.distribution']
        yaml_buffer['ep_operating_system']['distribution_major_version'] = initialization_form['ep_operating_system.distribution_major_version']
        yaml_buffer['ep_configuration']['keyboard_layout'] = initialization_form['ep_configuration.keyboard_layout']
        yaml_buffer['ep_configuration']['system_language'] = initialization_form['ep_configuration.system_language']
        save_yaml('/etc/bluebanquise/inventory/group_vars/all/equipment_all/equipment_profile.yml',yaml_buffer)

        print(str(yaml_buffer))
        return render_template("page.html.j2", page_content_path="content/initialize/report.html", page_title="Initialization - Report")

##### INVENTORY

### GROUPS

@app.route("/inventory/groups/index.html")
def inventory_groups_index():
    return render_template("page.html.j2", page_content_path="content/inventory/groups/index.html", page_title="Inventory - Groups", page_left_menu="content/inventory/groups/menu.html")



@app.route("/inventory/groups/master_groups/index.html", methods = ['GET', 'POST'])
def inventory_groups_master_groups_index():
    if request.method == 'POST':
        print(request.form)
        if "add_master_group_name" in request.form: # From add
            os.system('mkdir /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_master_group_name'))
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.form.get('add_master_group_name')+'/mg_data.yml',{'description':request.form.get('add_master_group_description')})
            os.system('touch /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_master_group_name')+'/mg_custom_variables.yml')
        if "manage_master_group_description" in request.form: # From manage
            print(request.args.get('master_group'))
            yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/'+request.args.get('master_group')+'/mg_data.yml')
            yaml_buffer['description'] = request.form.get('manage_master_group_description')
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.args.get('master_group')+'/mg_data.yml',yaml_buffer)
            save_yaml( '/etc/bluebanquise/inventory/group_vars/'+request.args.get('master_group')+'/mg_custom_variables.yml', yaml.safe_load(request.form.get('manage_master_group_variables')) )
    # Gather list of existing master groups
    master_groups_data = {}
    for folder in os.listdir("/etc/bluebanquise/inventory/group_vars/"):
        if re.match('^mg_', folder):
             yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/' + folder + '/mg_data.yml')
             master_groups_data[folder] = yaml_buffer
    return render_template("page.html.j2", page_content_path="content/inventory/groups/master_groups/index.html", page_title="Inventory - Groups", page_left_menu="content/inventory/groups/menu.html", left_menu_active="master_groups", master_groups_data=master_groups_data)

@app.route("/inventory/groups/master_groups/add.html")
def inventory_groups_master_groups_add():
    return render_template("page.html.j2", \
    page_content_path="content/inventory/groups/master_groups/add.html", \
    page_title="Inventory - Groups", \
    page_left_menu="content/inventory/groups/menu.html", \
    left_menu_active="master_groups" )

@app.route("/inventory/groups/master_groups/manage.html", methods = ['GET'])
def inventory_groups_master_groups_manage():
    if request.method == 'GET':
        master_group_data = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('master_group') + '/mg_data.yml')
        master_group_custom_variables = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('master_group') + '/mg_custom_variables.yml')
        print(master_group_custom_variables)
        return render_template("page.html.j2", page_content_path="content/inventory/groups/master_groups/manage.html", page_title="Inventory - Groups", \
        page_left_menu="content/inventory/groups/menu.html", left_menu_active="master_groups", \
        master_group_data=master_group_data, master_group_custom_variables=yaml.dump(master_group_custom_variables), master_group=request.args.get('master_group') )


@app.route("/inventory/groups/equipment_profile/index.html", methods = ['GET', 'POST'])
def inventory_groups_equipment_profile_groups_index():

    if request.method == 'POST':
        if "add_equipment_profile_group_name" in request.form:
            os.system('mkdir /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_equipment_profile_group_name'))
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.form.get('add_equipment_profile_group_name')+'/ep_data.yml',{'description':request.form.get('add_equipment_profile_group_description')})

    # Gather list of existing equipment_profile groups
    equipment_profile_groups_data = {}
    for folder in os.listdir("/etc/bluebanquise/inventory/group_vars/"):
        if re.match('^equipment_', folder):
             yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/' + folder + '/ep_data.yml')
             equipment_profile_groups_data[folder] = yaml_buffer
    print(equipment_profile_groups_data)
    return render_template("page.html.j2", page_content_path="content/inventory/groups/equipment_profile/index.html", page_title="Inventory - Groups", page_left_menu="content/inventory/groups/menu.html", left_menu_active="equipment_profile_groups", equipment_profile_groups_data=equipment_profile_groups_data)

@app.route("/inventory/groups/equipment_profile/add.html")
def inventory_groups_equipment_profile_groups_add():
    return render_template("page.html.j2", page_content_path="content/inventory/groups/equipment_profile/add.html", page_title="Inventory - Groups", page_left_menu="content/inventory/groups/menu.html", left_menu_active="equipment_profile_groups")


if __name__ == '__main__':
    app.run()
