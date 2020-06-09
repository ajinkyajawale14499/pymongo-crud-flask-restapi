from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify,request

from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key="secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email= _json['email']
    _password = _json['pwd']

    if _name and _password and _email and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert({
            'name' : _name,
            'email' : _email,
            'pwd': _hashed_password
        })
        response = jsonify("User added successfully"),200
        return response
    else:
        return not_found()

@app.route('/users',methods=['GET'])
def users():
    users = mongo.db.user.find()
    response = dumps(users)
    return response

@app.route('/users/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id' : ObjectId(id)})
    response = dumps(user)
    return response

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({
        '_id' : ObjectId(id)
    })
    response = jsonify("user deleted successfully"),202
    return response

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _password and _id and _email and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one(
            {
            '_id' : ObjectId( _id['$oid']) if 'oid' in _id else ObjectId(_id)
            },
            {
                '$set': {
                    'name' : _name,
                    'email' : _email,
                    'pwd' : _hashed_password,
                }
            }
        )
        response = jsonify('User updated successfully'),200
        return response


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status' : 404,
        'message':'Not Found'+ request.url
    }
    response = jsonify(message)
    return response



if __name__=='__main__':
    app.run(debug=True)