import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions import load_yaml,dump_yaml

master_groups = Blueprint('master_groups', __name__, template_folder='templates')

etc_path = 'B:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))

@master_groups.route("/inventory/master_groups/index.html", methods = ['GET'])
def inventory_master_groups_index():
    # Gather list of existing groups that are not all or equipment_ or mg_
    master_groups_data = {}
    for folder in os.listdir("etcbluebanquiseinventory/group_vars/"):
        if re.match('^mg_.*', folder):
             yaml_buffer = load_yaml('etcbluebanquiseinventory/group_vars/' + folder + '/data.yml')
             master_groups_data[folder] = yaml_buffer

    return render_template("page.html.j2", \
    page_content_path="groups/index.html.j2", \
    page_title="Inventory - Groups", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="groups/menu.html.j2", left_menu_active="index", \
    custom_groups_data=master_groups_data)

