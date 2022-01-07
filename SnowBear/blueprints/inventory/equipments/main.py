import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml

equipments = Blueprint('equipments', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@equipments.route("/inventory/equipments/index.html", methods = ['GET', 'POST'])
def inventory_equipments_index():

    # Gather list of existing equipment groups
    equipment_groups_data = {}
    for folder in os.listdir("etcbluebanquiseinventory/group_vars/"):
        if re.match('^equipment_.*', folder):
             yaml_buffer = load_yaml('etcbluebanquiseinventory/group_vars/' + folder + '/data.yml')
             equipment_groups_data[folder] = yaml_buffer

    return render_template("page.html.j2", \
    page_content_path="equipments/index.html.j2", \
    page_title="Inventory - Equipments", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="equipments/menu.html.j2", left_menu_active="index", \
    equipment_groups_data=equipment_groups_data)
