import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml,merge_default_current

parameters = Blueprint('parameters', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')

@parameters.route("/parameters/index.html", methods = ['GET', 'POST'])
def parameters_index():

    flags={'updated': False}
    if request.method == 'POST':
        buffer_dict = request.form.to_dict()
        dump_yaml('etcsnowbear/parameters.yml',buffer_dict)
        flags['updated'] = True


    parameters_variables_default = load_yaml('blueprints/parameters/parameters_variables.yml')
    # Check if file exist. It should, but in case of...
    file_exist = os.path.exists('etcsnowbear/parameters.yml')
    if not file_exist:
        parameters_variables = parameters_variables_default
    else:
        parameters_variables_current = load_yaml('etcsnowbear/parameters.yml')
        parameters_variables = merge_default_current(parameters_variables_default,parameters_variables_current)

    return render_template("page.html.j2", \
    page_content_path="parameters/index.html.j2", \
    page_title="Parameters", \
    page_navigation_data=page_navigation_data, \
    flags=flags, \
    parameters_variables=parameters_variables )
