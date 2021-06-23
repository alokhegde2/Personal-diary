from flask import Flask, request, jsonify, Blueprint
from datetime import date
import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

diary = Blueprint('diary', __name__)

# Pack


def pack(note_id, user_id, name, date, description):
    buf = str(note_id+'|'+user_id+'|'+name+'|'+date+'|'+description+'#')
    return buf

# unpack


def unpack(s):
    u = s.split('|')
    return u

# Writing data to file


def file_write(buf):
    with open(basedir+'/diary.txt', "a")as file:
        file.write(buf)
    file.close()

# To insert data


def insert(note_id, user_id, name, date, description):
    buf = pack(note_id, user_id, name, date, description)
    file_write(buf)

# Verify user id


def verify_user(id):
    new_path = os.path.join(basedir, '..\\auth\\user.txt')

    diary = []
    buf = ''
    flag = 0
    with open(new_path, "r+") as file:
        while True:
            ch = file.read(1)
            if not ch:
                break
            if ch != '#':
                buf = buf+ch
            else:
                fields = unpack(buf)
                if id == fields[0]:
                    flag = 1
                    return True
                buf = ''

        if flag == 0:
            file.close()
            return False

# All routes goes here

# to create new diary


@diary.route('/new', methods=["POST"])
def create():
    create_date = str(date.today())
    note_id = str(uuid.uuid1())
    name = request.json["name"]
    description = request.json["description"]
    user_id = request.json["user_id"]
    buf = ''
    flag = 0
    if request.method == 'POST':
        with open(basedir+'/diary.txt', "r") as file:
            while True:
                ch = file.read(1)
                if not ch:
                    break
                if ch != "#":
                    buf = buf+ch
                else:
                    fields = unpack(buf)
            if flag == 0:
                buf = pack(note_id, user_id, name, create_date, description)
                file_write(buf)
                return jsonify({"message": "success"}), 200


# to get all diary using user_id

@diary.route("/all-diary/<user_id>", methods=["GET"])
def getAllDiary(user_id):
    diary = []
    buf = ''
    flag = 0
    with open(basedir+'/diary.txt', "r") as file:
        while True:
            ch = file.read(1)
            if not ch:
                break
            if ch != '#':
                buf = buf+ch
            else:
                fields = unpack(buf)
                if not verify_user(user_id):
                    return jsonify(
                        message="User not found"
                    ), 400
                if user_id == fields[1]:
                    flag = 1
                    data = {
                        "note_id": fields[0],
                        "user_id": fields[1],
                        "name": fields[2],
                        "date": fields[3],
                        "description": fields[4]
                    }
                    diary.append(data)
                buf = ''
        if flag == 1:
            return jsonify(
                diary=diary
            ), 200
        if flag == 0:
            file.close()
            return jsonify(
                message="Record not found",
                status=404
            ), 404
