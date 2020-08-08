from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

################################################################

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.Apollo_Hospital
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print("ERROR - Cannot connect to database")

################################################################
@app.route("/users/<id>", methods=["PATCH"])

def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"email":request.form["email"]}}
            )
        #for attr in dir(dbResponse):
            #print(f"****{attr}****")
        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message":"Patient data updated"}),
                status=200,
                mimetype="application/json"
                )
        else:
            return Response(
                response= json.dumps({"message":"Nothing to update"}),
                status=200,
                mimetype="application/json"
                )
    except Exception as ex:
        print("*************************")
        print(ex)
        print("*************************")
        return Response(
            response= json.dumps({"message":"Sorry, cannot update patient data"}),
            status=500,
            mimetype="application/json"
            )


################################################################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message":"Cannot read patient data"}), status=500, mimetype="application/json")

################################################################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "firstname":request.form["firstname"],
            "lastname":request.form["lastname"],
             "age":request.form["age"],
             "gender":request.form["gender"],
             "email":request.form["email"],
             "phonenumber":request.form["phonenumber"]
             }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        #for attr in dir(dbresponse):
            #print(attr)
        return Response(
            response= json.dumps(
                {"message":"patient created", 
                 "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
            )
    except Exception as ex:
        print("********")
        print(ex)
        print("********")
################################################################
@app.route("/users/<id>", methods=["DELETE"])

def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        #for attr in dir(dbresponse):
            #print(f"****{attr}****")
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message":"patient data deleted",
                 "id":f"{id}"}),
                status=200,
                mimetype="application/json"
                )
        return Response(
            response= json.dumps(
                {"message":"patient data not available in database",
                 "id":f"{id}"
                }),
            status=200,
            mimetype="application/json"
            )

    except Exception as ex:
        print("********")
        print(ex)
        print("********")
        return Response(response= json.dumps({"message":"Cannot delete patient data"}), status=500, mimetype="application/json")
################################################################
if __name__ == "__main__":
    app.run(port=80, debug=True)