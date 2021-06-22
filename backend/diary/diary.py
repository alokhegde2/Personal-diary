from flask import Flask, request, jsonify,Blueprint
import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

diary = Blueprint('diary', __name__)

def pack(note_id,name,date,description):
	buf=str(note_id+'|'+name+'|'+date+'|'+description+'#')
	return buf

def unpack(s):
	u=s.split('|')
	return u

def file_write(buf):
	with open(basedir+'/diary.txt',"a")as file:
		file.write(buf)
	file.close()

def insert(note_id,name,date,description):
	buf=pack(note_id,name,date,description)
	file_write(buf)

#creating new diary

@diary.route('/new',methods=["POST"])
def create():
	note_id=str(uuid.uuid1())
	name=request.json["name"]
	date=request.json["date"]
	description=request.json["description"]
	buf=''
	flag=0
	if request.method=='POST':
		with open(basedir+'/diary.txt',"r") as file:
			while True:
				ch=file.read(1)
				if not ch:
					break
				if ch!="#":
					buf=buf+ch
				else:
					fields=unpack(buf)
			if flag==0:
				buf=pack(note_id,name,date,description)
				file_write(buf)
				return jsonify({"message": "success"}),200