import os
import re
from time import time
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
    if (os.path.isfile(absolute_path+"/group_vars/all/general_settings/network.yml") == True):
        print(absolute_path+"/group_vars/all/general_settings/network.yml")
        print("it exists")
        network_list=load_yaml(absolute_path+"/group_vars/all/general_settings/network.yml")["networks"]
    else:
        print("does not exist")
        open((absolute_path+"/group_vars/all/general_settings/network.yml"), 'a').close()
        dump_yaml(absolute_path+"/group_vars/all/general_settings/network.yml",{'domain_name': 'tumulus.local', 'networks': {'ice1-1': {'subnet': '10.10.0.0', 'prefix': 16, 'netmask': '255.255.0.0', 'broadcast': '10.10.255.255', 'dhcp_unknown_range': '10.10.254.1 10.10.254.254', 'gateway': '10.10.2.1', 'is_in_dhcp': True, 'is_in_dns': True, 'services_ip': {'pxe_ip': '10.10.0.1', 'dns_ip': '10.10.0.1', 'repository_ip': '10.10.0.1', 'authentication_ip': '10.10.0.1', 'time_ip': '10.10.0.1', 'log_ip': '10.10.0.1'}}}})
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
    if request.method== "POST":
        try:
            print("sucess")
            network_identifier=request.form.get("network_identifier")
            
            subnet=(request.form.get("subnet"))
            prefix=(request.form.get("prefix"))
            netmask=(request.form.get("netmask"))
            broadcast=(request.form.get("broadcast"))
            dhcp_unknown_range=(request.form.get("dhcp_unknow_range"))
            gateway=(request.form.get("gateway"))
            is_in_dhcp=(request.form.get("is_in_dhcp"))
            is_in_dns=(request.form.get("is_in_dns"))

            pxe_ip=(request.form.get("pxe_ip"))
            dns_ip=(request.form.get("dns_ip"))
            repository_ip=(request.form.get("repository_ip"))
            authentication_ip=(request.form.get("authentication_ip"))
            time_ip=(request.form.get("time_ip"))
            log_ip=(request.form.get("log_ip"))


            absolute_path=load_yaml("general_settings.yml")["general_settings"]["root_path"]
            yaml_buffer = load_yaml(absolute_path+"/group_vars/all/general_settings/network.yml")
            yaml_buffer['networks'][network_identifier] = {'subnet': subnet, 'prefix': prefix, 'netmask': netmask, 'broadcast': broadcast, 'dhcp_unknown_range': dhcp_unknown_range, 'gateway': gateway, 'is_in_dhcp': is_in_dhcp, 'is_in_dns': is_in_dns, 'services_ip': {'pxe_ip': pxe_ip, 'dns_ip': dns_ip, 'repository_ip': repository_ip, 'authentication_ip': authentication_ip, 'time_ip': time_ip, 'log_ip': log_ip}}

            dump_yaml(absolute_path+"/group_vars/all/general_settings/network.yml",yaml_buffer)
            return render_template("page.html.j2", \
            page_content_path="network/network_add.html.j2", \
            page_title="Inventory - network list", \
            page_navigation_data=page_navigation_data, \
            page_left_menu="network/menu.html.j2", left_menu_active="networks", \
            is_success="true", \
            )
        except: 
            return render_template("page.html.j2", \
            page_content_path="network/network_add.html.j2", \
            page_title="Inventory - network list", \
            page_navigation_data=page_navigation_data, \
            page_left_menu="network/menu.html.j2", left_menu_active="networks", \
            is_success="false", \
            )

        
    absolute_path=load_yaml("general_settings.yml")["general_settings"]["root_path"]
    network_list=load_yaml(absolute_path+"/group_vars/all/general_settings/network.yml")
    return render_template("page.html.j2", \
    page_content_path="network/network_add.html.j2", \
    page_title="Inventory - network list", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="network/menu.html.j2", left_menu_active="networks", \
    )