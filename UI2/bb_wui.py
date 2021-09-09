import subprocess
from subprocess import Popen, PIPE
import time
from flask import Flask, render_template, request, redirect, jsonify
import re
import os
import yaml
import json
import importlib


# Colors, from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_yaml(filename):
    print(bcolors.OKBLUE+'[INFO] Loading '+filename+bcolors.ENDC)
    with open(filename, 'r') as f:
        # return yaml.load(f, Loader=yaml.FullLoader) ## Waiting for PyYaml 5.1
        return yaml.load(f)

def save_yaml(filename,yaml_data):
    print(bcolors.OKBLUE+'[INFO] Dumping '+filename+bcolors.ENDC)
    with open(filename, 'w') as f:
        f.write(yaml.dump(yaml_data))
    return 0

app = Flask(__name__)

SERVICES = [
    {'path': 'blueprints.groups.main', 'blueprint': 'groups'},
    {'path': 'blueprints.initialize.main', 'blueprint': 'initialize'},
    {'path': 'blueprints.nodes.main', 'blueprint': 'nodes'},
]

for service in SERVICES:
    module = importlib.import_module(service['path'], package='app')
    app.register_blueprint(getattr(module, service['blueprint']))
#from blueprints.nodes.main import nodes
#importlib.import_module("blueprints.nodes.main")
#register_blueprints(app,"nodes","blueprints.nodes.main")


#app.register_blueprint(nodes)

initialization_form = None

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@app.route("/")
def index():
    return render_template("page.html.j2", page_content_path="content/index.html", page_title="Home")



##### INVENTORY

if __name__ == '__main__':
    app.run()
