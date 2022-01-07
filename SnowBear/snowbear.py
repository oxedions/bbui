#!/usr/bin/env python3

# ██████╗ ██╗     ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗██╗███████╗███████╗
# ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔═══██╗██║   ██║██║██╔════╝██╔════╝
# ██████╔╝██║     ██║   ██║█████╗  ██████╔╝███████║██╔██╗ ██║██║   ██║██║   ██║██║███████╗█████╗
# ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║▄▄ ██║██║   ██║██║╚════██║██╔══╝
# ██████╔╝███████╗╚██████╔╝███████╗██████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║███████║███████╗
# ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝

# SnowBear WebUI
# Benoit Leveugle <benoit.leveugle@gmail.com>

import logging
import subprocess
from subprocess import Popen, PIPE
import time
from flask import Flask, render_template, request, redirect, jsonify
import re
import os
import yaml
import json
import importlib
from functions.bbui import load_yaml,dump_yaml,load_page_navigation_data

app = Flask(__name__)

# Load main services
page_navigation_data = load_yaml('blueprints.yml')
## Gather blueprints navigation data
#page_navigation_data = load_page_navigation_data(page_navigation_data)

# Load blueprints
print('')
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

@app.route("/")
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

           _____                    ______                 
          /  ___|                   | ___ \                
          \ `--. _ __   _____      _| |_/ / ___  __ _ _ __ 
           `--. \ '_ \ / _ \ \ /\ / / ___ \/ _ \/ _` | '__|
          /\__/ / | | | (_) \ V  V /| |_/ /  __/ (_| | |   
          \____/|_| |_|\___/ \_/\_/ \____/ \___|\__,_|_|   
                                                
                                                    
                BlueBanquise WebUI
                v 1.0.0
    ''')

    app.run()
