import os
import yaml
import shutil
from flask import Blueprint, request, render_template



# Flask setup
groups_front = Blueprint('groups_front', __name__, template_folder='templates')


@groups_front.route("/inventory/groups/add_fn_group", methods=["GET"])
def add_fn_group():
  return render_template("page.html.j2", page_body="groups/add_fn_group.html", page_title="Add function group", left_menu="inventory/menu.html", navbar_active="home")

@groups_front.route("/inventory/groups/add_os_group", methods=["GET"])
def add_os_group():
  return render_template("page.html.j2", page_body="groups/add_os_group.html", page_title="Add function group", left_menu="inventory/menu.html", navbar_active="home")

@groups_front.route("/inventory/groups/add_hw_group", methods=["GET"])
def add_hw_group():
  return render_template("page.html.j2", page_body="groups/add_hw_group.html", page_title="Add function group", left_menu="inventory/menu.html", navbar_active="home")
