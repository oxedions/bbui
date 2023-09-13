import os
import re
import yaml
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from functions import load_yaml,dump_yaml,merge_default_current,mergearrays
import requests

etc_path = 'I:\polarbear\etc'

parameters = Blueprint('parameters', __name__, template_folder='templates')

@parameters.route("/v1/parameters", methods=["GET"])
def parameters_get(): # Provide parameters
    # Check if parameters file exist
    # - if not, return empty
    # - if yes, we load the file content
    file_exist = os.path.exists(os.path.join(etc_path,'parameters.yml'))
    if not file_exist:
        polarbear_parameters = {}
    else:
        polarbear_parameters = load_yaml(os.path.join(etc_path,'parameters.yml'))

    return jsonify(polarbear_parameters), 200

@parameters.route("/v1/parameters", methods=["POST"])
def parameters_post(): # Update parameters
    dump_yaml(os.path.join(etc_path,'parameters.yml'),request.get_json())
    return "OK", 200
