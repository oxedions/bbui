import os
import re
import yaml
import json
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from functions import load_yaml,dump_yaml,merge_default_current,mergearrays
import requests

parameters = Blueprint('parameters', __name__, template_folder='templates')

etc_path = 'B:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))

@parameters.route("/parameters/index.html", methods = ['GET'])
def parameters_index():

    flags={'status': None}
    # Grab status if it was passed as arguments
    if 'status' in request.args:
        if request.args['status'] == "updated":
            flags['status'] = "updated"
        if request.args['status'] == "error":
            flags['status'] = "error"

    # Grab page content
    polarbear_parameters_default = load_yaml('blueprints/parameters/parameters_fields.yml')
    # Grab current parameters from backend
    polarbear_parameters_current = requests.get("http://localhost:5001/v1/parameters")
    # Update page content with current parameters: merge both with current precedence default
    polarbear_parameters = merge_default_current(polarbear_parameters_default, polarbear_parameters_current.json())

    return render_template("page.html.j2", \
    page_content_path="parameters/index.html.j2", \
    page_title="Parameters", \
    page_navigation_data=page_navigation_data, \
    flags=flags, \
    parameters_variables=polarbear_parameters )

@parameters.route("/parameters", methods = ['POST'])
def parameters_post():
    backend_response = requests.post("http://localhost:5001/v1/parameters", json=mergearrays(request.form))
    if backend_response.status_code == 200:
        return redirect(url_for("parameters.parameters_index", status="updated"))
    else:
        return redirect(url_for("parameters.parameters_index", status="error"))


