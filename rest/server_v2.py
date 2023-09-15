from argparse import ArgumentParser
import os
import yaml
import json
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import importlib

# Get arguments passed to bootset
parser = ArgumentParser()
parser.add_argument("-s", "--server", dest="server",
                    help="Enable or disable server mode", metavar="NODE", default=False)

passed_arguments, cli_request = parser.parse_known_args()

#passed_arguments = parser.parse_args()

to_load_blueprints = []
for file_path in os.listdir('blueprints'):
    # check if current file_path is a file
    if os.path.isfile(os.path.join('blueprints', file_path)):
        to_load_blueprints.append(file_path.replace('.py', ''))

if passed_arguments.server:
    app = Flask(__name__)
    api = Api(app)

    for to_load_blueprint in to_load_blueprints:
        print("Loading '" + to_load_blueprint + "' blueprint")
        bmodule = importlib.import_module('blueprints.' + to_load_blueprint, package='app')
        app.register_blueprint(getattr(bmodule, to_load_blueprint))
    print("URLs map:")
    print(app.url_map)

    print("Now running as server")
    app.run(debug=True)

else:
    dyn_modules = {}
    for to_load_blueprint in to_load_blueprints:
        print("Loading '" + to_load_blueprint + "' blueprint")
        dyn_modules[to_load_blueprint] = importlib.import_module('blueprints.' + to_load_blueprint)
    cli_method = cli_request[0]
    if cli_method not in ['get', 'post', 'delete', 'put']:
        print('Error, unknown ' + str(cli_method) + ' method')
        quit()
    cli_url = cli_request[1]
    if len(cli_request[2:]) > 0 and cli_request[2:] is not None:
        cli_data = ' '.join(cli_request[2:])
    else:
        print("Using empty data")
        cli_data = "{}"
    print(cli_url.split('/')[0])
    print(cli_method)
    print(cli_url)
    print(cli_data)
    call_message, call_http_code = dyn_modules[cli_url.split('/')[0]].cli_main(cli_method, cli_url, cli_data)
    print("Code: " + str(call_http_code))
    print("Message :\n")
    # Try to convert message to yaml for better output
    try:
        print(yaml.safe_dump(call_message, allow_unicode=True, default_flow_style=False))
    except:
        print(str(call_message))
    finally:
        quit()

    #print(getattr(dyn_modules[cli_url.split('/')[0]], 'cli_' + cli_url.replace('/', '_') + '_resource_' + cli_method)(cli_data))
    #print("running as client")
    #resource_name = "nodes"
    #ressource_method = "get"
    #eval('print(module.cli_nodes_resource_get()))
    #print(globals())
    #print(globals()["module"].cli_nodes_resource_get())
    #print(cli_nodes_resource_get())


quit()
