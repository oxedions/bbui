import os
import re
import yaml
import json
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from functions import load_yaml,dump_yaml,merge_default_current,mergearrays
import requests

parameters = Blueprint('parameters', __name__, template_folder='templates')

etc_path = 'C:\polarbear\etc'
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))

##########################################################################################
########################################################################################
######################################################################################
################## FRONTEND
################
##############

@parameters.route("/parameters/index.html", methods = ['GET'])
def parameters_front():

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
    polarbear_parameters_current = parameters_back_get()
    # Update page content with current parameters: merge both with current precedence default
    polarbear_parameters = merge_default_current(polarbear_parameters_default, polarbear_parameters_current)

    return render_template("page.html.j2", \
    page_content_path="parameters/index.html.j2", \
    page_title="Parameters", \
    page_navigation_data=page_navigation_data, \
    flags=flags, \
    parameters_variables=polarbear_parameters )

@parameters.route("/parameters", methods = ['POST'])
def parameters_front_post():
    parameters_back_post(mergearrays(request.form))
    return redirect(url_for("parameters.parameters_front", status="updated"))

##########################################################################################
########################################################################################
######################################################################################
################## BACKEND - API
################
##############

##############
### GET
##############
def parameters_back_get():
    # Check if parameters file exist
    # - if not, return empty
    # - if yes, we load the file content
    file_exist = os.path.exists(os.path.join(etc_path,'parameters.yml'))
    if not file_exist:
        polarbear_parameters = {}
    else:
        polarbear_parameters = load_yaml(os.path.join(etc_path,'parameters.yml'))
    return polarbear_parameters

@parameters.route("/v1/parameters", methods=["GET"])
def parameters_back_get_api():
    return jsonify(parameters_back_get()), 200

##############
### POST
##############
def parameters_back_post(yaml_data): # Update parameters
    dump_yaml(os.path.join(etc_path,'parameters.yml'),yaml_data)

@parameters.route("/v1/parameters", methods=["POST"])
def parameters_back_post_api():
    parameters_back_post(request.get_json())
    return "OK", 200
