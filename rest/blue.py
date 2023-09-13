import os
import re
import yaml
from flask import Blueprint, render_template, request,jsonify
from flask_restful import Api, Resource, url_for

blue = Blueprint('blue', __name__)
bapi = Api(blue)

class bluetest(Resource):
    def get(self):
        return str(testy(1,2)), 200

bapi.add_resource(bluetest, '/test')

def testy(a,b):
    return a+b
