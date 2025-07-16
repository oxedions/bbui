import os
import yaml
import shutil
from flask import Blueprint, request, render_template



# Flask setup
groups_front = Blueprint('groups_front', __name__, template_folder='templates')

@groups_front.route("/inventory/groups/fn_groups", methods=["GET"])
def fn_groups():
  return render_template("page.html.j2", page_body="groups/fn_groups.html", page_title="Manage function groups", left_menu="inventory/menu.html", left_menu_active="fn_groups", navbar_active="inventory")

@groups_front.route("/inventory/groups/fn_group", methods=["GET"])
def fn_group():
  return render_template("page.html.j2", page_body="groups/fn_group.html", page_title="Manage function group", left_menu="inventory/menu.html", left_menu_active="fn_groups", navbar_active="inventory")

@groups_front.route("/inventory/groups/add_fn_group", methods=["GET"])
def add_fn_group():
  return render_template("page.html.j2", page_body="groups/add_fn_group.html", page_title="Add function group", left_menu="inventory/menu.html", left_menu_active="fn_groups", navbar_active="inventory")

@groups_front.route("/inventory/groups/os_groups", methods=["GET"])
def os_groups():
  return render_template("page.html.j2", page_body="groups/os_groups.html", page_title="Manage function group", left_menu="inventory/menu.html", left_menu_active="os_groups", navbar_active="inventory")

@groups_front.route("/inventory/groups/os_group", methods=["GET"])
def os_group():
  return render_template("page.html.j2", page_body="groups/os_group.html", page_title="Manage os group", left_menu="inventory/menu.html", left_menu_active="os_groups", navbar_active="inventory")

@groups_front.route("/inventory/groups/add_os_group", methods=["GET"])
def add_os_group():
  return render_template("page.html.j2", page_body="groups/add_os_group.html", page_title="Add os group", left_menu="inventory/menu.html", left_menu_active="os_groups", navbar_active="inventory")


@groups_front.route("/inventory/groups/add_hw_group", methods=["GET"])
def add_hw_group():
  return render_template("page.html.j2", page_body="groups/add_hw_group.html", page_title="Add hardware group", left_menu="inventory/menu.html", left_menu_active="hw_groups", navbar_active="inventory")
