import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml

network = Blueprint('network', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@network.route("/inventory/network/index.html", methods = ['GET', 'POST'])
def inventory_network_index():

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

@network.route("/inventory/equipment/add.html")
def inventory_equipment_add():

    equipment_variables = load_yaml('blueprints/inventory/equipment/equipment_variables.yml')

    return render_template("page.html.j2", \
    page_content_path="equipment/add.html.j2", \
    page_title="Inventory - equipment - Add", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="equipment/menu.html.j2", left_menu_active="add", \
    equipment_variables=equipment_variables ) 