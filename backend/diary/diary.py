from flask import Flask, request, jsonify,Blueprint
import os
import uuid


basedir = os.path.abspath(os.path.dirname(__file__))
diary = Blueprint('diary', __name__)