#This is the main file please write all your codes here by cloning this repo
# from backend.auth.login import login_user
from flask import Flask, request, jsonify

import flask
from auth.auth import auth



# Init app
app = Flask(__name__)


#register all your routes here

app.register_blueprint(auth,url_prefix="/user")



# Run Server
if __name__ == '__main__':
  app.run(debug=True)