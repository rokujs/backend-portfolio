from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson import json_util
from flask_cors import CORS, cross_origin
import os

load_dotenv()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = os.getenv('MONGO')


mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def homepage():
  return jsonify({
    "message": "my first API with flask"
  })

@app.route('/messages', methods=['GET'])
def get_all_message():
  messages = mongo.db.msg.find()
  response = json_util.dumps(messages)
  
  return Response(response, mimetype='application/json')

@app.route('/message', methods=['POST'])
@cross_origin()
def create_new_message():
  print(request.json)
  name = request.json['name']
  email = request.json['email']
  message = request.json['message']

  if name and email and message:
    mongo.db.msg.insert({
      'name': name,
      'email': email,
      'msg': message
    })

    response = jsonify({
      'message': "Create message",
    })

    response.status_code = 201

    return response

  return 'nana'

@app.errorhandler(400)
def not_found(error=None):
  res = jsonify({
    'message': 'Resource not found',
    'status': 404
  })

  res.status_code = 404

  return res

if __name__ == '__main__':
  app.run(debug = False)