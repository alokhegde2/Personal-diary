#This is the main file please write all your codes here by cloning this repo
from flask import Flask, request, jsonify
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#pack(),unpack(),search() functions

#buffer
global buf

#pack()

def pack(usn,name,branch,sem):
  buf=usn+'|'+name+'|'+branch+'|'+sem+'#'
  return buf

#unpack()  

def unpack(s):
  ind=s.split('|')
  return ind

#file_write()

def file_write(buf):
  with open("var.txt","a") as file:
    file.write(buf)
  file.close()

#insert()

def insert():
  usn = input("enter usn\t")
  name = input("enter name\t")
  branch= input("enter branch\t")
  sem = input("enter semester\t")
  buf=pack(usn,name,branch,sem)
  file_write(buf)

# Create the routes here

#register a user route
@app.route('/user/register',methods= ["GET"])
def register_user():
  file = open(basedir+'/test.txt','r')
  return file.read()
  
@app.route('/user/<id>',methods = ["GET"])
def getUserDetails(id):
  # file = open(basedir+'/test.txt','r')
  # return file.read()
  buf=''
  flag=0
  # key=id
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