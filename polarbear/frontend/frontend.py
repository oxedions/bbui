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

etc_path = 'C:\polarbear\etc'

# Load blueprints
print('')
page_navigation_data = load_yaml(os.path.join(etc_path,'frontend_blueprints.yml'))
if page_navigation_data is not None and page_navigation_data:
    for navigation in page_navigation_data:
        if 'sub_navigation' in navigation:
            for sub_navigation in navigation['sub_navigation']:
                if sub_navigation['name'] != 'navbar-divider':
                    print(' * Importing blueprint "' + str(sub_navigation['name']) + '"')
                    module = importlib.import_module('blueprints.' + str(navigation['name']) + '.' + str(sub_navigation['name']) + '.main', package='app')
                    app.register_blueprint(getattr(module, sub_navigation['name']))
        else:
            print(' * Importing blueprint ' + str(navigation['name']))
            module = importlib.import_module('blueprints.' + str(navigation['name']) + '.main', package='app')
            app.register_blueprint(getattr(module, navigation['name']))
print('')

print(' * Importing parameters' )
module = importlib.import_module('blueprints.parameters.main', package='app')
app.register_blueprint(getattr(module, 'parameters'))


@app.route("/", methods=["GET","POST"])
def index():
    return render_template("page.html.j2", page_content_path="home/index.html.j2", page_title="Home", page_navigation_data=page_navigation_data)





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

                BlueBanquise PolarBear FrontEnd
                v 1.0.0
    ''')

    app.run()
