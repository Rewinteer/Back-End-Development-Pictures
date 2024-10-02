from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

def id_already_exists(id):
    for entry in data:
        if entry["id"] == id:
            return True

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for entry in data:
        if entry["id"] == id:
            return entry, 200
    return {"message": "wrong id"}, 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    if not new_pic:
        return {"Message": "Wrong Data"}, 400
    elif id_already_exists(new_pic['id']):
        return {"Message": f"picture with id {new_pic['id']} already present"}, 302
    data.append(new_pic)
    return new_pic, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.get_json()
    if not new_pic:
        return {"Message": "Wrong Data"}, 400
    
    for i in range(len(data)):
        if new_pic["id"] == data[i]["id"]:
            data[i] = new_pic
            return {"Message": "The data successfully updated"}, 200
    return {"Message": "picture not found"}, 404
        


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for entry in data:
        if entry['id'] == id:
            data.remove(entry)
            return ("", 204)
    return {"message": "picture not found"}, 404
