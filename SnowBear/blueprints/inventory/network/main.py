import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml


network = Blueprint('network', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@network.route("/inventory/network/index.html", methods = ['GET', 'POST'])
def inventory_network_index():
    return render_template("page.html.j2", \
    page_content_path="network/index.html.j2", \
    page_title="Inventory - network", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="network/menu.html.j2", left_menu_active="networks", \
    )

@network.route("/inventory/network/networks.html", methods = ['GET', 'POST'])
def inventory_network_networks():
    absolute_path=load_yaml("general_settings.yml")["general_settings"]["root_path"]
    network_list=load_yaml(absolute_path+"/group_vars/all/general_settings/network.yml")["networks"]
    return render_template("page.html.j2", \
    page_content_path="network/networks.html.j2", \
    page_title="Inventory - networks", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="network/menu.html.j2", left_menu_active="networks", \
    network_list=network_list, \
    )

@network.route("/inventory/network/network_add.html", methods = ['GET', 'POST'])
def inventory_network_network_add():
    absolute_path=load_yaml("general_settings.yml")["general_settings"]["root_path"]
    network_list=load_yaml(absolute_path+"/group_vars/all/general_settings/network.yml")
    return render_template("page.html.j2", \
    page_content_path="network/network_add.html.j2", \
    page_title="Inventory - network list", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="network/menu.html.j2", left_menu_active="networks", \
    )