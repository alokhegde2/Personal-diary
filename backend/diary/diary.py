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

# Delete diary


def delete_diary(note_id,user_id):
    data = []
    buf = ''
    flag = 0
    with open(basedir+'/diary.txt', "r+") as file:
        while True:
            ch = file.read(1)
            if not ch:
                break
            if ch != '#':
                buf = buf+ch
            else:
                fields = unpack(buf)
                data.append(fields)
                buf = ''
        for i in data:
            if i[0] == note_id and i[1] == user_id:
                index = data.index(i)
                data.pop(index)
                file.truncate(0)
                for lines in data:
                    insert(lines[0], lines[1], lines[2], lines[3], lines[4])
                break
        return "success"
        if flag == 0:
            file.close()
            return "error"

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

# to check diary name already in list


def check_list(note_id, diary):
    for i in range(0, len(diary)):
        if diary[i]["note_id"] == note_id:
            return False
    return True

# All routes goes here

# to create new diary


@diary.route('/new-diary', methods=["POST"])
def create():
    created_date = str(date.today())
    note_id = str(uuid.uuid1())
    name = request.json["title"]
    description = request.json["description"]
    user_id = request.json["user_id"]
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
                    flag = 1
                    return jsonify(
                        message="User not found"
                    ), 400
                buf = ''
        if flag == 0:

            buf = pack(note_id, user_id, name, created_date, description)
            file_write(buf)
            return jsonify(
                message="Diary Created"
            ), 200

# to get single diary using note_id


@diary.route('/single-diary/<note_id>/<user_id>', methods=["GET"])
def search(note_id, user_id):
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
                if note_id == fields[0]:
                    flag = 1
                    return jsonify(
                        user_id=fields[1],
                        note_id=fields[0],
                        name=fields[2],
                        created_date=fields[3],
                        description=fields[4]
                    ), 200
                buf = ''
        if flag == 0:
            file.close()
            return jsonify(message="Diary not found"), 404

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
            ), 400


# Update the single diary

@diary.route("/update-diary/<noteId>/<userId>", methods=["PUT"])
def updateDiary(noteId, userId):
    note_id = noteId
    user_id = userId
    name = request.json["title"]
    created_date = str(date.today())
    description = request.json["description"]
    buf = ''
    flag = 0
    key = noteId
    with open(basedir+'/diary.txt', "r+") as file:
        while True:
            ch = file.read(1)
            if not ch:
                break
            if ch != '#':
                buf = buf+ch
            else:
                fields = unpack(buf)
                if not verify_user(userId):
                    return jsonify(
                        message="User not found"
                    ), 400
                if key == fields[0] and user_id == fields[1]:
                    flag = 1
                    insert(note_id, user_id, name, created_date, description)
                    res = delete_diary(noteId,user_id)
                    if res == "error" :
                        return jsonify(
                            message="Diary not deleted"
                        ), 400
                    return jsonify(
                        message="Diary updated"
                    ), 200
                buf = ''
    if flag == 0:
        return jsonify(
            message="Diary not found"
        ), 400
    file.close()


# To Delete single diary

@diary.route("/delete-diary/<noteId>/<userId>", methods=["DELETE"])
def deleteDiary(noteId, userId):
    if not verify_user(userId):
        return jsonify(
            message="User not found"
        ), 400
    response = delete_diary(noteId,userId)
    if response == "success":
        return jsonify(
            message="Diary deleted"
        ), 200
    if response == "error":
        return jsonify(
            message="Diary not deleted"
        ), 400


# To search diary using date

@diary.route("/search-by/date/<userId>", methods=["POST"])
def searchDiaryByDate(userId):
    diary = []
    created_date = request.json["created_date"]
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
                if not verify_user(userId):
                    return jsonify(
                        message="User not found"
                    ), 400
                if userId == fields[1]:
                    if created_date == fields[3]:
                        if check_list(fields[0], diary):
                            flag = 1
                            data = {
                                "note_id": fields[0],
                                "user_id": fields[1],
                                "name": fields[2],
                                "date": fields[3],
                                "description": fields[4]
                            }
                            diary.append(data)
                        else:
                            continue
                buf = ''
        if len(diary) == 0:
            return jsonify(
                message="No results found"
            ), 400
        if flag == 1:
            return jsonify(
                diary=diary
            ), 200
        if flag == 0:
            file.close()
            return jsonify(
                message="Record not found",
            ), 400


# To search diary using diary name

@diary.route("/search-by/name/<userId>", methods=["POST"])
def searchDiaryByName(userId):
    diary = []
    name = str(request.json["name"])
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
                if not verify_user(userId):
                    return jsonify(
                        message="User not found"
                    ), 400
                if userId == fields[1]:
                    if name.lower() in fields[2].lower():
                        if check_list(fields[0], diary):
                            flag = 1
                            data = {
                                "note_id": fields[0],
                                "user_id": fields[1],
                                "name": fields[2],
                                "date": fields[3],
                                "description": fields[4]
                            }
                            diary.append(data)
                        else:
                            continue
                buf = ''
        if len(diary) == 0:
            return jsonify(
                message="No results found"
            ), 400
        if flag == 1:
            return jsonify(
                diary=diary
            ), 200
        if flag == 0:
            file.close()
            return jsonify(
                message="Record not found",
            ), 400
