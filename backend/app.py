#This is the main file please write all your codes here by cloning this repo
from flask import Flask, request, jsonify
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


# Create the routes here










# Run Server
if __name__ == '__main__':
  app.run(debug=True)