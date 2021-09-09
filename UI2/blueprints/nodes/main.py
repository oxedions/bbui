from flask import Blueprint, render_template
from functions.bbui import load_yaml

nodes = Blueprint('nodes', __name__, template_folder='templates')

@nodes.route('/inventory/nodes/index.html')
def nodes_index():
    return render_template("page.html.j2", page_content_path="nodes/index.html", page_title="Inventory - Nodes", page_left_menu="nodes/menu.html")

@nodes.route('/inventory/nodes/add.html')
def nodes_add():
    return render_template("page.html.j2", page_content_path="nodes/add.html", page_title="Inventory - Add Nodes", page_left_menu="nodes/menu.html")
