import os
import yaml
import shutil
from flask import Blueprint, request, render_template



# Flask setup
inventory = Blueprint('inventory', __name__, template_folder='templates')


@inventory.route("/inventory", methods=["GET"])
def inventory_index():
  return render_template("page.html.j2", page_body="inventory/index.html", page_title="Inventory", left_menu="inventory/menu.html", navbar_active="home")
