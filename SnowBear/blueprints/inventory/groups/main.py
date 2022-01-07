import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml

groups = Blueprint('groups', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@groups.route("/inventory/groups/index.html", methods = ['GET', 'POST'])
def inventory_groups_index():

    if request.method == 'POST':
        print(request.form)
        if "add_custom_group_name" in request.form: # From add
            folder_exist = os.path.exists('etcbluebanquiseinventory/group_vars/'+request.form.get('add_custom_group_name'))
            if not folder_exist:
                os.makedirs('etcbluebanquiseinventory/group_vars/'+request.form.get('add_custom_group_name'))
                dump_yaml('etcbluebanquiseinventory/group_vars/'+request.form.get('add_custom_group_name')+'/data.yml',{'description':request.form.get('add_custom_group_description')})
                os.close(os.open('etcbluebanquiseinventory/group_vars/'+request.form.get('add_custom_group_name')+'/variables.yml', os.O_CREAT))
        if "manage_custom_group_description" in request.form: # From manage
            yaml_buffer = load_yaml('etcbluebanquiseinventory/group_vars/'+request.args.get('custom_group')+'/data.yml')
            yaml_buffer['description'] = request.form.get('manage_custom_group_description')
            dump_yaml('etcbluebanquiseinventory/group_vars/'+request.args.get('custom_group')+'/data.yml',yaml_buffer)
            if len(str(request.form.get('manage_custom_group_variables'))) != 0:
                dump_yaml( 'etcbluebanquiseinventory/group_vars/'+request.args.get('custom_group')+'/variables.yml', yaml.safe_load(request.form.get('manage_custom_group_variables')) )

    # Gather list of existing groups that are not all or equipment_ or mg_
    custom_groups_data = {}
    for folder in os.listdir("etcbluebanquiseinventory/group_vars/"):
        if not re.match('^equipment_.*', folder) and not re.match('^all$', folder) and not re.match('^mg_.*', folder):
             yaml_buffer = load_yaml('etcbluebanquiseinventory/group_vars/' + folder + '/data.yml')
             custom_groups_data[folder] = yaml_buffer

    return render_template("page.html.j2", \
    page_content_path="groups/index.html.j2", \
    page_title="Inventory - Groups", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="groups/menu.html.j2", left_menu_active="index", \
    custom_groups_data=custom_groups_data)


@groups.route("/inventory/groups/add.html")
def inventory_groups_add():

    return render_template("page.html.j2", \
    page_content_path="groups/add.html.j2", \
    page_title="Inventory - Groups - Add", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="groups/menu.html.j2", left_menu_active="add")


@groups.route("/inventory/groups/manage.html", methods = ['GET'])
def inventory_groups_manage():

    if request.method == 'GET':
        custom_group_data = load_yaml('etcbluebanquiseinventory/group_vars/' + request.args.get('custom_group') + '/data.yml')
        custom_group_variables = load_yaml('etcbluebanquiseinventory/group_vars/' + request.args.get('custom_group') + '/variables.yml')
        if str(custom_group_variables) == 'None':
            custom_group_variables = ''
        else:
            custom_group_variables = yaml.dump(custom_group_variables)

        return render_template("page.html.j2", \
        page_content_path="groups/manage.html.j2", \
        page_title="Inventory - Groups - Manage", \
        page_navigation_data=page_navigation_data, \
        page_left_menu="groups/menu.html.j2", left_menu_active="manage", \
        custom_group=request.args.get('custom_group'), \
        custom_group_data=custom_group_data, \
        custom_group_variables=custom_group_variables)