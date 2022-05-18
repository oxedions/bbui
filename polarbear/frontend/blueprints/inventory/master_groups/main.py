import os
import re
import yaml
from flask import Blueprint, render_template, request, redirect, url_for
from functions import load_yaml,dump_yaml,mergearrays
import requests


master_groups = Blueprint('master_groups', __name__, template_folder='templates')

etc_path = 'B:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))

@master_groups.route("/inventory/master_groups/index.html", methods = ['GET'])
def inventory_master_groups_index():

    flags={'status': None}
    # Grab status if it was passed as arguments
    if 'status' in request.args:
        if request.args['status'] == "updated":
            flags['status'] = "updated"
        if request.args['status'] == "error":
            flags['status'] = "error"
    
    # Request list of master groups and their data from backend
    master_groups_dict = requests.get("http://localhost:5001/v1/inventory/master_groups")

    return render_template("page.html.j2", \
    page_content_path="master_groups/index.html.j2", \
    page_title="Inventory - Master Groups", \
    page_navigation_data=page_navigation_data, \
    page_left_menu="master_groups/menu.html.j2", left_menu_active="index", \
    master_groups_dict=master_groups_dict)

@master_groups.route("/inventory/master_groups", methods = ['POST'])
def master_groups_post():
    # Send new group to backend, and wait for answer
    backend_response = requests.post("http://localhost:5001/v1/inventory/master_groups", json=mergearrays(request.form))
    if backend_response.status_code == 200:
        return redirect(url_for("master_groups.inventory_master_groups_index", status="updated"))
    else:
        return redirect(url_for("master_groups.inventory_master_groups_index", status="error"))
