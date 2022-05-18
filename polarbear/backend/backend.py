#!/usr/bin/env python3

# ██████╗ ██╗     ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗██╗███████╗███████╗
# ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔═══██╗██║   ██║██║██╔════╝██╔════╝
# ██████╔╝██║     ██║   ██║█████╗  ██████╔╝███████║██╔██╗ ██║██║   ██║██║   ██║██║███████╗█████╗
# ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║▄▄ ██║██║   ██║██║╚════██║██╔══╝
# ██████╔╝███████╗╚██████╔╝███████╗██████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║███████║███████╗
# ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝

# PolarBear WebUI
# Benoit Leveugle <benoit.leveugle@gmail.com>

from flask import Flask, render_template, request, redirect, jsonify

from functions import load_yaml,dump_yaml,load_page_navigation_data,update_yaml

import os
import yaml
import importlib


app = Flask(__name__)

etc_path = 'B:\polarbear\etc'

# Load blueprints
print('')
blueprints_list = load_yaml(os.path.join(etc_path,'backend_blueprints.yml'))
if blueprints_list is not None and blueprints_list:
    for blueprint in blueprints_list:
        print(' * Importing blueprint ' + str(blueprint))
        module = importlib.import_module('blueprints.' + str(blueprint) + ".main", package='app')
        app.register_blueprint(getattr(module, blueprint.split(".")[-1]))
print('')

print(' * Importing parameters' )
module = importlib.import_module('blueprints.parameters.main', package='app')
app.register_blueprint(getattr(module, 'parameters'))

@app.route("/", methods=["GET"])
def index():
  return "Backend is alive"

if __name__ == '__main__':
    print('''
                             _.--""""--.._
                         _.""    ."       `-._
                       .";      ;           ; `-.
                      / /     ."           ;     `.
                     / ;     ;             ;       \\
                    ; :      :             :     `-.\\
                    ; ;      :              `.      `;
                    : :      :                \      :
                    : \      `:                \   `.;
                     \ \      `;                ;    ;
                      \ : ."   ;                |   ;
                       `>"     :              `.;   )
                       / _."               `.  ;/ _(
                      ;,"     ;    `.        `.;    `-.
                     ;" ."   :    `. `.       / \, \ \ \\
                     :,"     :      `. `. \  ; ::\_/_/_/::
                   .-=:.-"  -,-   "-.,=-.\ ;.; :::; ; ;::
                   |(`.`     :       .")| \: `.  :::::::
                    \\/      :       \//   ;   \              _____
                     :      .:.       :  _/     ;             \hjw:
           /         ;                ;  ;      |              \"""
         ."          :    _     _    ;  /       ;              /|
        /             `.  \;   ;/  ." ."       /              /:|
       |                !  :   :  !_."        /           .--::/
       |\___             `.:   :."/\         ;      ____.":|:|/
       \:::|\              \ _ /  | :       :   ___/|:::|:""""
        `""|:\             ;"^"   | !       :__/|::|/""""
           \::\_____     .-"      | ;       |::|/""
            \:|::::|\   / / /    / /       /"""
             \|::::|:`--\_\_\__."-|       ;
               """" \::::::::::::/      ."
                     """"""""".-"      (
              __,------.__.--/ , ,  , |/--._
             /              :\|  |  |v"     \_
            |\              :::v-;v-"::       \\
            \:\              :::::::::         \\
             \|`-.                             /|
               `: \          ____         ____/:/
                 \|:-.______/|::|\       /|:::|/
                  |::|:::::|:/"""\\_____/:/""""
                  `-:|:::::|/     \|::::|/
                     `""""""       `"""""

                BlueBanquise PolarBear Backend
                v 1.0.0
    ''')

    app.run(port=5001)
