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
import os.path
from os import path
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


def insertFile(yamlFile,yamlPath,data):
  """This function inserts yaml data into a file
  
  Args:
      yamlFile ([string]): path to the file to write to
      yamlPath ([String]): list of the path to get to the attribute
      data ([string]): data that you want to insert into the path in the file. 

      for example, if your file looks like this :       
        general_settings:
          root_path: 

      then insertFile("file.yml",['general_settings','root_path'],test)      
      will result in your file looking like this:
      general_settings:
          root_path: test

  """
  if(len(yamlPath)==2):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  elif(len(yamlPath)==3):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]][yamlPath[2]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  elif(len(yamlPath)==4):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]][yamlPath[2]][yamlPath[3]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  else:
    print("Path superior to 4 is not supported")
  
def readFile(yamlFile):
  """this functions returns a dictionnary of the yaml file in order to get values from it

  Args:
      yamlFile (string): Path to the yaml file to parse

  Returns:
      [dictionnary]: dictionnary with the values of the file
  """
  stream=open(yamlFile,'r')
  fileData=yaml.safe_load(stream)
  return fileData




@app.route("/", methods=["GET","POST"])
def index():
    if request.method== "POST":
      full_path=request.form.get("full_path")
      #check if the path exists 
      if (path.exists(str(full_path))):
        insertFile("general_settings.yml",['general_settings','root_path'],str(full_path))
        return render_template("page.html.j2", page_content_path="home/index.html.j2", page_title="Home", page_navigation_data=page_navigation_data, path_check="Given path exists and will be used")
      print("checked"+full_path)
      return render_template("page.html.j2", page_content_path="home/index.html.j2", page_title="Home", page_navigation_data=page_navigation_data, path_check="Given path does not exist")
    return render_template("page.html.j2", page_content_path="home/index.html.j2", page_title="Home", page_navigation_data=page_navigation_data, path_check="Please enter a path")

if __name__ == '__main__':
    print("loading configuration with the following parameters:")
    print(readFile("general_settings.yml"))
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
