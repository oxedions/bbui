import subprocess
from subprocess import Popen, PIPE
import time
from flask import Flask, render_template, request, redirect, jsonify
import re
import os
import yaml

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

app = Flask(__name__)

initialization_form = None

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@app.route("/")
def index():
    return render_template("page.html.j2", page_content_path="content/index.html", page_title="Home")

##### INITIALIZE

@app.route("/initialize/index.html")
def initialize_index():
    return render_template("page.html.j2", page_content_path="content/initialize/index.html", page_title="Initialize")

@app.route("/initialize/start.html")
def initialize_start():
    return render_template("page.html.j2", page_content_path="content/initialize/start.html", page_title="Start initialization")

@app.route("/initialize/step_2.html", methods = ['POST'])
def initialize_step_2():

    global initialization_form

    if request.method == 'POST':
        initialization_form = {}
        print('initialize_step_2 POST')
        print(request.form)
        initialization_form = request.form.to_dict()
        print('Value' + str(initialization_form))
        return render_template("page.html.j2", page_content_path="content/initialize/step_2.html", page_title="Start initialization")

@app.route("/initialize/step_3.html", methods = ['POST'])
def initialize_step_3():

    global initialization_form

    if request.method == 'POST':
        print('initialize_step_3 POST')
        print(request.form)
        initialization_form = Merge(initialization_form,request.form.to_dict())
        print('Value' + str(initialization_form))
        return "coucou"



if __name__ == '__main__':
    app.run()
