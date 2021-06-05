# from __main__ import basedir
from flask import Flask, request, jsonify,Blueprint
import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))
auth = Blueprint('auth', __name__)

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
          if password == fields[2]:
            return jsonify(
              message = "Login success"
            ),200
          return jsonify(
            message = "Password is not matching"
          ),403
        buf=''
    if flag==0:
      print("\n\n\nrecord doesnt exist")
      file.close()
      return  jsonify(
        status="Email not found",
      ),404


#register a user route
@auth.route('/register',methods= ["POST"])
def register_user():
  email = request.json['email']
  name = request.json['name']
  password = request.json['password']
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
            password = fields[2],
            mail = fields[3],
          ),200
        buf=''
    if flag==0:
      file.close()
      return  jsonify(
        message="Record doesnt exist",
        status=404
      ),404

# @auth.route('/changepass',methods=["POST"])
# def changePassword():
#   old_password = request.json['old_password']
#   new_password = request.json['new_password']
#   user_id = request.json['user_id']
#   buf=''
#   flag=0
#   key=user_id
#   with open(basedir+'/user.txt',"r+") as file:
#     while True:
#       ch=file.read(1)
#       if not ch:
#           break
#       if ch!='#':
#           buf=buf+ch
#       else:
#           fields=unpack(buf)
#           if key== fields[0]:
#             if old_password != fields[2]:
#               return jsonify(
#                 status="error",
#                 message="Password not matching"
#                 ),400

                
#             flag=1
#             prev=file.tell()
#             lenbuf=len(buf)
#             file.seek(prev-lenbuf-1,0)
#             c='*'
#             file.write(c)
#             file.close()
#             insert(user_id,fields[1],new_password,fields[3])
#             return jsonify(
#               status = "Successs",
#               message = "User updated"
#                )
#           buf=''
#   if flag==0:
#     return jsonify(
#       status = "error",
#       message = "User not updated"
#       )
#   file.close()


@auth.route('/changepass',methods=["POST"])
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
      # elif ch.strip("#") != old_password:
      #   file.write(ch)
      if ch!='#':
          buf=buf+ch
      else:
          fields=unpack(buf)
          if key== fields[0]:
            if old_password != fields[2]:
              return jsonify(
                status="error",
                message="Password not matching"
                ),400

            if ch.strip("#") != old_password:
              file.write(ch)   
            flag=1
            insert(user_id,fields[1],new_password,fields[3])
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