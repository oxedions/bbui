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

process_id = None
process_step = None
working_form = None

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

#### Initialize

@app.route("/initialize")
def initialize():
    return render_template("initialize.html")

@app.route("/initialize_running", methods = ['GET', 'POST'])
def initialize_running():

    global process_id
    global process_step
    global working_form

    print('Processing page initialize_running with method: '+request.method)

#    if "clear_existing_inventory" in request.form:
#        clear_existing_inventory = True
#    if "add_example" in request.form:
    if request.method == 'POST':
        print('Entering POST section')
        print(request.form)
        print('Start')

        process_step = 0
        working_form = request.form
        return render_template("initialize_running.html")

    if request.method == 'GET':
        print('Entering GET section')

        if process_step == 0:
            process_id = subprocess.Popen('echo "executing scripts/initialize/step_0.sh" >>/var/log/bb_wui.log; bash -x scripts/initialize/step_0.sh >>/var/log/bb_wui.log 2>&1', shell=True)
            process_step = 1
            return jsonify(process_status = 1, process_step = process_step)
        else:
            retcode = process_id.poll()
            if retcode is not None: # Process finished.
                if process_step == 1: # Second process to launch now
                    process_id = subprocess.Popen('mkdir /etc/bluebanquise/inventory/group_vars/all/ -p; mkdir /etc/bluebanquise/inventory/cluster; mkdir /etc/bluebanquise/inventory/groups; cp -a /etc/bluebanquise/resources/examples/simple_cluster/inventory/group_vars/all/* /etc/bluebanquise/inventory/group_vars/all/; rm -f /etc/bluebanquise/inventory/group_vars/all/networks/*; sync; sleep 1s', shell=True)
                    process_step = 2
                    return jsonify(process_status = 1, process_step = process_step)
                if process_step == 2: # Second process to launch now
                    process_id = subprocess.Popen('sed -i "s/cluster_name:\ algoric/cluster_name:\ '+working_form.get('cluster_name')+'/g" /etc/bluebanquise/inventory/group_vars/all/general_settings/general.yml; sync; sleep 1s', shell=True)
                    process_step = 3
                    return jsonify(process_status = 1, process_step = process_step)
                else: # All tasks ended, allow exiting
                    return jsonify(process_status = 0, process_step = process_step)
            else: # No process is done, wait a bit and check again.
                return jsonify(process_status = 1, process_step = process_step)

#### Groups management

@app.route("/inventory_management/groups/masters", methods = ['GET', 'POST'])
def inventory_management_groups_masters():

    if request.method == 'POST':
        if "add_master_group_name" in request.form:
            os.system('mkdir /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_master_group_name'))
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.form.get('add_master_group_name')+'/mg_data.yml',{'details':request.form.get('add_master_group_info')})

    # Gather list of existing master groups
    mg_group_list = []
    for folder in os.listdir("/etc/bluebanquise/inventory/group_vars/"):
        if re.match('^mg_', folder):
             mg_group_list.append(folder)
    return render_template("inventory_management/groups/masters/masters.html",mg_group_list=mg_group_list)

@app.route("/inventory_management/groups/masters/add")
def inventory_management_groups_masters_add():
    return render_template("inventory_management/groups/masters/add.html")


#### Groups equipment

@app.route("/inventory_management/groups/equipment", methods = ['GET', 'POST'])
def inventory_management_groups_equipment():

    if request.method == 'POST':
        if "add_equipment_group_name" in request.form:
            os.system('mkdir /etc/bluebanquise/inventory/group_vars/'+request.form.get('add_equipment_group_name'))
            save_yaml('/etc/bluebanquise/inventory/group_vars/'+request.form.get('add_equipment_group_name')+'/equipment_data.yml',{'details':request.form.get('add_equipment_group_info')})


    # Gather list of existing equipment groups
    eq_group_list = []
    for folder in os.listdir("/etc/bluebanquise/inventory/group_vars/"):
        if re.match('^equipment_', folder):
             eq_group_list.append(folder)
    return render_template("inventory_management/groups/equipment/equipment.html",eq_group_list=eq_group_list)

@app.route("/inventory_management/groups/equipment/add")
def inventory_management_groups_equipment_add():
    return render_template("inventory_management/groups/equipment/add.html")


@app.route("/load_node_log")
def tutu():
    print(request.method)
    stdout, stderr = subprocess.Popen("tail -200 /var/log/dnf.log", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
    return str(stdout).replace('\\n','<br>').replace('b"','').replace('<br>"','')

@app.route("/main_log")
def main_log():
    print(request.method)
    stdout, stderr = subprocess.Popen("tail -200 /var/log/bb_wui.log", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
    return str(stdout).replace('\\n','<br>').replace('b"','').replace('<br>"','')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()


# trash
#
# @app.route("/try")
# def trytry():
#     return render_template("try.html")
#
# @app.route("/coucou")
# def coucou():
#     return "you did it!"
#
# @app.route("/ajax")
# def ajax():
#     return render_template("ajax.html")



#         for i in range(1, 20):
#             retcode = process_id.poll()
#             if retcode is not None: # Process finished.
#                 print("done")
#                 break
#             else: # No process is done, wait a bit and check again.
#                 print("waiting"+str(i))
#                 time.sleep(1)
#                 continue
#        return redirect(request.url)

#         print(process_id)
#         for i in range(1, 20):
#             retcode = process_id.poll()
#             if retcode is not None: # Process finished.
#                 print("done")
#                 break
#             else: # No process is done, wait a bit and check again.
#                 print("waiting"+str(i))
#                 time.sleep(1)
#                 return redirect(request.url)
# #                continue
#         print("ok")
#    print(request.form.get('cluster_name'))
#    print(request.form)
#    for toto in request.form:
#        print(toto)
#         return redirect(request.url)
#     if request.method == 'GET':
# #        global process_id
#         print('Go into GET')
#         print(process_id)
#         for i in range(1, 20):
#             retcode = process_id.poll()
#             if retcode is not None: # Process finished.
#                 print("done")
#                 break
#             else: # No process is done, wait a bit and check again.
#                 print("waiting"+str(i))
#                 time.sleep(1)
#                 continue
#
#     print(request.method)
#     return "running"
