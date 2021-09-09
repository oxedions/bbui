import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,save_yaml

groups = Blueprint('groups', __name__, template_folder='templates')

@groups.route("/inventory/groups/index.html")
def inventory_groups_index():
    return render_template("page.html.j2", page_content_path="groups/index.html", page_title="Inventory - Groups", page_left_menu="groups/menu.html")

### MASTER GROUPS

@groups.route("/inventory/groups/master_groups/index.html", methods = ['GET', 'POST'])
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
    return render_template("page.html.j2", page_content_path="groups/master_groups/index.html", page_title="Inventory - Groups", page_left_menu="groups/menu.html", left_menu_active="master_groups", master_groups_data=master_groups_data)

@groups.route("/inventory/groups/master_groups/add.html")
def inventory_groups_master_groups_add():
    return render_template("page.html.j2", \
    page_content_path="groups/master_groups/add.html", \
    page_title="Inventory - Groups", \
    page_left_menu="groups/menu.html", \
    left_menu_active="master_groups" )

@groups.route("/inventory/groups/master_groups/manage.html", methods = ['GET'])
def inventory_groups_master_groups_manage():
    if request.method == 'GET':
        master_group_data = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('master_group') + '/mg_data.yml')
        master_group_custom_variables = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('master_group') + '/mg_custom_variables.yml')
        print(master_group_custom_variables)
        return render_template("page.html.j2", page_content_path="groups/master_groups/manage.html", page_title="Inventory - Groups", \
        page_left_menu="groups/menu.html", left_menu_active="master_groups", \
        master_group_data=master_group_data, master_group_custom_variables=yaml.dump(master_group_custom_variables), master_group=request.args.get('master_group') )

### CUSTOM GROUPS

@groups.route("/inventory/groups/custom_groups/index.html", methods = ['GET', 'POST'])
def inventory_groups_custom_groups_index():
    if request.method == 'POST':
        print(request.form)
        if "add_custom_group_name" in request.form: # From add
            os.system('mkdir /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_custom_group_name'))
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.form.get('add_custom_group_name')+'/mg_data.yml',{'description':request.form.get('add_custom_group_description')})
            os.system('touch /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_custom_group_name')+'/mg_custom_variables.yml')
        if "manage_custom_group_description" in request.form: # From manage
            print(request.args.get('custom_group'))
            yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/'+request.args.get('custom_group')+'/mg_data.yml')
            yaml_buffer['description'] = request.form.get('manage_custom_group_description')
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.args.get('custom_group')+'/mg_data.yml',yaml_buffer)
            save_yaml( '/etc/bluebanquise/inventory/group_vars/'+request.args.get('custom_group')+'/mg_custom_variables.yml', yaml.safe_load(request.form.get('manage_custom_group_variables')) )
    # Gather list of existing custom groups
    custom_groups_data = {}
    for folder in os.listdir("/etc/bluebanquise/inventory/group_vars/"):
        if re.match('^custom_', folder):
             yaml_buffer = load_yaml('/etc/bluebanquise/inventory/group_vars/' + folder + '/mg_data.yml')
             custom_groups_data[folder] = yaml_buffer
    return render_template("page.html.j2", page_content_path="groups/custom_groups/index.html", page_title="Inventory - Groups", page_left_menu="groups/menu.html", left_menu_active="custom_groups", custom_groups_data=custom_groups_data)

@groups.route("/inventory/groups/custom_groups/add.html")
def inventory_groups_custom_groups_add():
    return render_template("page.html.j2", \
    page_content_path="groups/custom_groups/add.html", \
    page_title="Inventory - Groups", \
    page_left_menu="groups/menu.html", \
    left_menu_active="custom_groups" )

@groups.route("/inventory/groups/custom_groups/manage.html", methods = ['GET'])
def inventory_groups_custom_groups_manage():
    if request.method == 'GET':
        custom_group_data = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('custom_group') + '/mg_data.yml')
        custom_group_custom_variables = load_yaml('/etc/bluebanquise/inventory/group_vars/' + request.args.get('custom_group') + '/mg_custom_variables.yml')
        print(custom_group_custom_variables)
        return render_template("page.html.j2", page_content_path="groups/custom_groups/manage.html", page_title="Inventory - Groups", \
        page_left_menu="groups/menu.html", left_menu_active="custom_groups", \
        custom_group_data=custom_group_data, custom_group_custom_variables=yaml.dump(custom_group_custom_variables), custom_group=request.args.get('custom_group') )


### EQUIPMENT_PROFILES

@groups.route("/inventory/groups/equipment_profile/index.html", methods = ['GET', 'POST'])
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
    return render_template("page.html.j2", page_content_path="groups/equipment_profile/index.html", page_title="Inventory - Groups", page_left_menu="groups/menu.html", left_menu_active="equipment_profile_groups", equipment_profile_groups_data=equipment_profile_groups_data)

@groups.route("/inventory/groups/equipment_profile/add.html")
def inventory_groups_equipment_profile_groups_add():
    return render_template("page.html.j2", page_content_path="groups/equipment_profile/add.html", page_title="Inventory - Groups", page_left_menu="groups/menu.html", left_menu_active="equipment_profile_groups")
