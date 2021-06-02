#This is the main file please write all your codes here by cloning this repo
from flask import Flask, request, jsonify
import os
import uuid


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#pack(),unpack(),search() functions

#buffer
global buf

#pack()

def pack(user_id,name,password,email):
  buf=user_id+'|'+name+'|'+password+'|'+email+'#'
  return buf

#unpack()  

def unpack(s):
  ind=s.split('|')
  return ind

#file_write()

def file_write(buf):
  with open(basedir+"/test.txt","a") as file:
    file.write(buf)
  file.close()

#insert()

def insert(user_id,name,password,email):
  buf=pack(user_id,name,password,email)
  file_write(buf)


# Create the routes here

#register a user route
@app.route('/user/register',methods= ["POST"])
def register_user():
  email = request.json['email']
  name = request.json['name']
  password = request.json['password']
  user_id = uuid.uuid1()
  buf=''
  flag=0
  with open(basedir+'/test.txt',"r") as file:
    while True:
      ch=file.read(1)
      if not ch:
        break
      if ch!='#':
        buf=buf+ch
      else:
        fields=unpack(buf)
        if email == fields[3]:
          print("record found\n")
          flag=1
          return jsonify(
            email = email,
            error ="Email already exists"
          ),409
        buf=''
    if flag==0:
      print("\n\n\nrecord doesnt exist")
      buf=pack(user_id,name,password,email)
      file_write(buf)
      return jsonify(
        status = "Successs",
        message = "New user created"
      )



#to get the single user details

@app.route('/user/<id>',methods = ["GET"])
def getUserDetails(id):
  buf=''
  flag=0
  with open(basedir+'/test.txt',"r") as file:
    while True:
      ch=file.read(1)
      if not ch:
        break
      if ch!='#':
        buf=buf+ch
      else:
        fields=unpack(buf)
        if id == fields[0]:
          print("record found\n")
          flag=1
          return jsonify(
            id = fields[0],
            name = fields[1],
            password = fields[2],
            mail = fields[3],
          )
        buf=''
    if flag==0:
      print("\n\n\nrecord doesnt exist")
      file.close()
      return  jsonify(
        category="error",
        status=404
      ),404




# Run Server
if __name__ == '__main__':
  app.run(debug=True)