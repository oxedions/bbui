import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,save_yaml

initialize = Blueprint('initialize', __name__, template_folder='templates')

##### INITIALIZE

@initialize.route("/initialize/index.html")
def initialize_index():
    return render_template("page.html.j2", page_content_path="initialize/index.html", page_title="Initialize")

@initialize.route("/initialize/step_1.html")
def initialize_step_1():
    print('initialize_step_1')
    return render_template("page.html.j2", page_content_path="initialize/step_1.html", page_title="Initialization - Step 1")

@initialize.route("/initialize/step_2.html", methods = ['POST'])
def initialize_step_2():

    global initialization_form

    if request.method == 'POST':
        initialization_form = {}
        print('initialize_step_2 POST')
        print(request.form)
        initialization_form = request.form.to_dict()
        print('Value' + str(initialization_form))
        return render_template("page.html.j2", page_content_path="initialize/step_2.html", page_title="Initialization - Step 2")

@initialize.route("/initialize/step_3.html", methods = ['POST'])
def initialize_step_3():

    global initialization_form

    if request.method == 'POST':
        print('initialize_step_3 POST')
        print(request.form)
        initialization_form = Merge(initialization_form,request.form.to_dict())
        print('Value' + str(initialization_form))
        return render_template("page.html.j2", page_content_path="initialize/step_3.html", page_title="Initialization - Step 3")

@initialize.route("/initialize/report.html", methods = ['POST'])
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
        return render_template("page.html.j2", page_content_path="initialize/report.html", page_title="Initialization - Report")
