# from __main__ import basedir
from flask import Flask, request, jsonify,Blueprint
import os
import uuid
from flask_bcrypt import generate_password_hash,check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
auth = Blueprint('auth', __name__)
# bcrypt = Bcrypt(app)

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
  with open(basedir+"/user.txt","a") as file:
    file.write(buf)
  file.close()


#insert()

def insert(user_id,name,password,email):
  buf=pack(user_id,name,password,email)
  file_write(buf)


#delete
def delete_user(user_id):
  test = []
  buf=''
  flag=0
  with open(basedir+'/user.txt',"r+") as file:
    while True:
      ch=file.read(1)
      if not ch:
        break
      if ch!='#':
        buf=buf+ch
      else:
        fields=unpack(buf)
        test.append(fields)
        buf=''
    for i in test:
      if(i[0] == user_id):
        index = test.index(i)
        test.pop(index)
        file.truncate(0)
        for lines in test:
          insert(lines[0],lines[1],lines[2],lines[3])
        break
    return jsonify(
      message="User Deleted"
      ),200
    if flag==0:
      file.close()
      return  jsonify(
        message="Record doesnt exist",
        status=404
      ),404


@auth.route('/login',methods = ["POST"])
def login_user():
  email = request.json["email"]
  password = request.json["password"]
  buf=''
  flag=0
  with open(basedir+'/user.txt',"r") as file:
    while True:
      ch=file.read(1)
      if not ch:
        break
      if ch!='#':
        buf=buf+ch
      else:
        fields=unpack(buf)
        if email == fields[3]:
          if check_password_hash(bytes(fields[2],"utf-8"),password):
            return jsonify(
              user_id = fields[0],
              message = "Login success"
            ),200
          return jsonify(
            message = "Incorrect Password"
          ),403
        buf=''
    if flag==0:
      file.close()
      return  jsonify(
        message="Email not found",
      ),404


#register a user route
@auth.route('/register',methods= ["POST"])
def register_user():
  email = request.json['email']
  name = request.json['name']
  password = generate_password_hash(request.json['password']).decode('utf-8')
  user_id = str(uuid.uuid1())
  buf=''
  flag=0
  with open(basedir+'/user.txt',"r") as file:
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
      ),200



#to get the single user details

@auth.route('/<id>',methods = ["GET"])
def getUserDetails(id):
  buf=''
  flag=0
  with open(basedir+'/user.txt',"r") as file:
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
            mail = fields[3],
          ),200
        buf=''
    if flag==0:
      file.close()
      return  jsonify(
        message="Record doesnt exist",
        status=404
      ),404

# Changing password

@auth.route('/changepass',methods=["PUT"])
def changePassword():
  old_password = request.json['old_password']
  new_password = request.json['new_password']
  user_id = request.json['user_id']
  buf=''
  flag=0
  key=user_id
  with open(basedir+'/user.txt',"r+") as file:
    while True:
      ch=file.read(1)
      if not ch:
          break
      if ch!='#':
          buf=buf+ch
      else:
          fields=unpack(buf)
          if key== fields[0]:
            if not check_password_hash(bytes(fields[2],"utf-8"),old_password):
              return jsonify(
                status="error",
                message="Password not matching"
                ),400
            flag=1
            new_password = generate_password_hash(request.json['new_password']).decode('utf-8')
            insert(user_id,fields[1],new_password,fields[3])
            delete_user(request.json['user_id'])
            return jsonify(
              status = "Successs",
              message = "User updated"
               )
          buf=''
  if flag==0:
    return jsonify(
      status = "error",
      message = "User not updated"
      )
  file.close()


#Deleting user

@auth.route('/delete-user',methods=["POST"])
def delete():
  test = []
  buf=''
  flag=0
  with open(basedir+'/user.txt',"r+") as file:
    while True:
      ch=file.read(1)
      if not ch:
        break
      if ch!='#':
        buf=buf+ch
      else:
        fields=unpack(buf)
        test.append(fields)
        buf=''
    for i in test:
      if(i[0] == request.json["user_id"]):
        index = test.index(i)
        test.pop(index)
        file.truncate(0)
        for lines in test:
          insert(lines[0],lines[1],lines[2],lines[3])
    return jsonify(
      message="User Deleted"
      ),200
    if flag==0:
      file.close()
      return  jsonify(
        message="Record doesnt exist",
        status=404
      ),404