import os
import re
import yaml
from flask import Blueprint, render_template, request
from functions.bbui import load_yaml,dump_yaml

tim = Blueprint('tim', __name__, template_folder='templates')

page_navigation_data = load_yaml('blueprints.yml')


@tim.route("/inventory/tim/index.html")
def inventory_tim_index():
    return render_template("coucou.html.j2", message="Salut les copains")