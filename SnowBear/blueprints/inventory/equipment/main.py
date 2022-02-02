import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml

equipment = Blueprint('equipment', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@equipment.route("/inventory/equipment/index.html", methods = ['GET', 'POST'])
def inventory_equipment_index():

    if request.method == 'POST':
        print(request.form)
        if "add_equipment_name" in request.form: # From add
            folder_exist = os.path.exists('etcbluebanquiseinventory/group_vars/equipment_'+request.form.get('add_equipment_name'))
            if not folder_exist:
                os.makedirs('etcbluebanquiseinventory/group_vars/equipment_'+request.form.get('add_equipment_name'))
                buffer_dict = request.form.to_dict()
                del(buffer_dict['add_equipment_name'])
                dump_yaml('etcbluebanquiseinventory/group_vars/equipment_'+request.form.get('add_equipment_name')+'/data.yml',buffer_dict)
                os.close(os.open('etcbluebanquiseinventory/group_vars/equipment_'+request.form.get('add_equipment_name')+'/variables.yml', os.O_CREAT))

    # Gather list of existing equipment groups
    equipment_groups_data = {}
    for folder in os.listdir("etcbluebanquiseinventory/group_vars/"):
        if re.match('^equipment_.*', folder):
             yaml_buffer = load_yaml('etcbluebanquiseinventory/group_vars/' + folder + '/data.yml')
             equipment_groups_data[folder] = yaml_buffer

    return render_template("page.html.j2", \
    page_content_path="equipment/index.html.j2", \
    page_title="Inventory - equipment", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="equipment/menu.html.j2", left_menu_active="index", \
    equipment_groups_data=equipment_groups_data)

@equipment.route("/inventory/equipment/add.html")
def inventory_equipment_add():

    equipment_variables = load_yaml('blueprints/inventory/equipment/equipment_variables.yml')

    return render_template("page.html.j2", \
    page_content_path="equipment/add.html.j2", \
    page_title="Inventory - equipment - Add", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="equipment/menu.html.j2", left_menu_active="add", \
    equipment_variables=equipment_variables )