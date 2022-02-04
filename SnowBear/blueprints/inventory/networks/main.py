import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml,demultiplex,merge_default_current

networks = Blueprint('networks', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@networks.route("/inventory/networks/index.html", methods = ['GET', 'POST'])
def inventory_networks_index():

    # Gather list of existing networks
    file_exist = os.path.exists('etcbluebanquiseinventory/group_vars/all/general_settings/networks.yml')
    if not file_exist:
        networks_data = {}
    else:
        networks_data = load_yaml('etcbluebanquiseinventory/group_vars/all/general_settings/networks.yml')

    flags={'event': None}
    if request.method == 'POST':
        buffer_dict = demultiplex(request.form.to_dict())
        print(buffer_dict)
        if 'add_network_name' in  buffer_dict:
            flags={'event': 'added'}
            add_network_name = buffer_dict['add_network_name']
            del(buffer_dict['add_network_name'])
            if not 'networks' in networks_data:
                networks_data={'networks':{}}
            networks_data['networks'][add_network_name] = buffer_dict
            dump_yaml('etcbluebanquiseinventory/group_vars/all/general_settings/networks.yml',networks_data)
        if 'managed_network_name' in  buffer_dict:
            print('managed')
            flags={'event': 'modified'}
            managed_network_name = buffer_dict['managed_network_name']
            del(buffer_dict['managed_network_name'])
            del(networks_data['networks'][managed_network_name])
            networks_data['networks'][managed_network_name] = buffer_dict
            dump_yaml('etcbluebanquiseinventory/group_vars/all/general_settings/networks.yml',networks_data)

    return render_template("page.html.j2", \
    page_content_path="networks/index.html.j2", \
    page_title="Cluster Networks", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="networks/menu.html.j2", left_menu_active="index", \
    flags=flags, \
    networks_data=networks_data)

@networks.route("/inventory/networks/add.html")
def inventory_networks_add():

    networks_variables = load_yaml('blueprints/inventory/networks/networks_variables.yml')

    return render_template("page.html.j2", \
    page_content_path="networks/add.html.j2", \
    page_title="Cluster Networks - Add", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="networks/menu.html.j2", left_menu_active="add", \
    networks_variables=networks_variables ) 

@networks.route("/inventory/networks/manage.html", methods = ['GET'])
def inventory_networks_manage():

    managed_network = request.args.get('managed_network')
    networks_variables = load_yaml('blueprints/inventory/networks/networks_variables.yml')
    networks_data = load_yaml('etcbluebanquiseinventory/group_vars/all/general_settings/networks.yml')

    networks_variables = merge_default_current(networks_variables,networks_data['networks'][managed_network])

    return render_template("page.html.j2", \
    page_content_path="networks/manage.html.j2", \
    page_title="Cluster Networks - Manage", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="networks/menu.html.j2", left_menu_active="manage", \
    managed_network=managed_network, \
    networks_variables=networks_variables)