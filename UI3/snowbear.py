#!/usr/bin/env python3

# ██████╗ ██╗     ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗██╗███████╗███████╗
# ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔═══██╗██║   ██║██║██╔════╝██╔════╝
# ██████╔╝██║     ██║   ██║█████╗  ██████╔╝███████║██╔██╗ ██║██║   ██║██║   ██║██║███████╗█████╗
# ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║▄▄ ██║██║   ██║██║╚════██║██╔══╝
# ██████╔╝███████╗╚██████╔╝███████╗██████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║███████║███████╗
# ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝

# SnowBear WebUI
# Benoit Leveugle <benoit.leveugle@gmail.com>

# import logging
# import subprocess
# from subprocess import Popen, PIPE
# import time
from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
# import os.path
# from os import path
# import re
import os
import yaml
import json
import importlib
# from functions.bbui import load_yaml,dump_yaml,load_page_navigation_data,update_yaml

app = Flask(__name__)

# Load blueprints
print('')
with open('blueprints.yml', 'r') as f:
  to_load_blueprints = yaml.safe_load(f)
for bname, bpath in to_load_blueprints.items():
        print('Importing blueprint ' + str(bname))
        module = importlib.import_module(str(bpath).replace('/','.') + '.main', package='app')
        app.register_blueprint(getattr(module, str(bname)))
print('')

@app.route('/webfonts/<path:filename>')
def cover_webfonts(filename):
  return send_from_directory(app.root_path + '/static/webfonts/', filename)

@app.route("/", methods=["GET"])
def index():
  return render_template("page.html.j2", page_body="home/body.html", left_menu="home/menu.html", page_title="Home", navbar_active="home")

if __name__ == '__main__':
    print('''
                             _.--""""--.._
                         _.""    ."       `-._
                       .";      ;           ; `-.
                      / /     ."           ;     `.
                     / ;     ;             ;       \\
                    ; :      :             :     `-.\\
                    ; ;      :              `.      `;
                    : :      :                \\      :
                    : \\      `:                \\   `.;
                     \\ \\      `;                ;    ;
                      \\ : ."   ;                |   ;
                       `>"     :              `.;   )
                       / _."               `.  ;/ _(
                      ;,"     ;    `.        `.;    `-.
                     ;" ."   :    `. `.       / \\, \\ \\ \\
                     :,"     :      `. `. \\  ; ::\\_/_/_/::
                   .-=:.-"  -,-   "-.,=-.\\ ;.; :::; ; ;::
                   |(`.`     :       .")| \\: `.  :::::::
                    \\/      :       \\//   ;   \\              _____
                     :      .:.       :  _/     ;             \\hjw:
           /         ;                ;  ;      |              \\"""
         ."          :    _     _    ;  /       ;              /|
        /             `.  \\;   ;/  ." ."       /              /:|
       |                !  :   :  !_."        /           .--::/
       |\\___             `.:   :."/\\         ;      ____.":|:|/
       \\:::|\\              \\ _ /  | :       :   ___/|:::|:""""
        `""|:\\             ;"^"   | !       :__/|::|/""""
           \\::\\_____     .-"      | ;       |::|/""
            \\:|::::|\\   / / /    / /       /"""
             \\|::::|:`--\\_\\_\\__."-|       ;
               """" \\::::::::::::/      ."
                     """"""""".-"      (
              __,------.__.--/ , ,  , |/--._
             /              :\\|  |  |v"     \\_
            |\\              :::v-;v-"::       \\
            \\:\\              :::::::::         \\
             \\|`-.                             /|
               `: \\          ____         ____/:/
                 \\|:-.______/|::|\\       /|:::|/
                  |::|:::::|:/"""\\_____/:/""""
                  `-:|:::::|/     \\|::::|/
                     `""""""       `"""""

           _____                    ______                 
          /  ___|                   | ___ \\                
          \\ `--. _ __   _____      _| |_/ / ___  __ _ _ __ 
           `--. \\ '_ \\ / _ \\ \\ /\\ / / ___ \\/ _ \\/ _` | '__|
          /\\__/ / | | | (_) \\ V  V /| |_/ /  __/ (_| | |   
          \\____/|_| |_|\\___/ \\_/\\_/ \\____/ \\___|\\__,_|_|    
                                                
                                                    
                BlueBanquise WebUI
                v 1.0.0
    ''')

    print("URLs map:")
    print(app.url_map)

    app.run()
