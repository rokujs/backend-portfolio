from bson.objectid import ObjectId
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson import json_util
from flask_cors import CORS, cross_origin
import os

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = os.getenv('MONGO')


mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def homepage():
  return jsonify({
    "message": "my first API with flask"
  })

@app.route('/projects', methods=['GET'])
def get_all_projects():
  projects = mongo.db.projects.find()
  response = json_util.dumps(projects)

  return Response(response, mimetype='application/json')

@app.route('/projects/<project_id>', methods=['GET'])
@cross_origin()
def get_project(project_id):
  project = mongo.db.projects.find({'_id': ObjectId(project_id)})
  if project:
    response = json_util.dumps(project)
    return Response(response, mimetype='application/json')

  return jsonify({
    "message": "Project not found"
  }), 404

@app.route('/project', methods=['POST'])
@cross_origin()
def add_project():
    title = request.json['title']
    images = request.json['images']
    technologies = request.json['technologies']
    link = request.json['link']
    code = request.json['code']
    colorBg = request.json['colorBg']
    description = request.json['description']

    if title and images and technologies and link and code and colorBg and description:
        mongo.db.projects.insert({
            'title': title,
            'images': images,
            'technologies': technologies,
            'link': link,
            'code': code,
            'colorBg': colorBg,
            'description': description
        })
        response = jsonify({'project': 'project added successfully!'})
        response.status_code = 200
        return response

    return 'error'


@app.route('/messages', methods=['GET'])
def get_all_message():
  messages = mongo.db.msg.find()
  response = json_util.dumps(messages)
  
  return Response(response, mimetype='application/json')

@app.route('/message', methods=['POST'])
@cross_origin()
def create_new_message():
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

  return 'message'

# list all skills
@app.route('/skills', methods=['GET'])
def get_all_skills():
  messages = mongo.db.skills.find()
  response = json_util.dumps(messages)
  
  return Response(response, mimetype='application/json')

# create new skill
@app.route('/skill', methods=['POST'])
@cross_origin()
def create_new_skill():
  name = request.json['name']
  color = request.json['color']
  percentage = request.json['percentage']
  icon = request.json['icon']
  category = request.json['category']

  skill_id = ""
  skill_arr = ""
  skills = list(mongo.db.skills.find())

  for skill in skills:
    if skill['category'] == category:
      skill_id = skill['_id']
      skill_arr = skill['technologies']
      skill_arr.append({
          'name': name,
          'color': color,
          'percentage': percentage,
          'icon': icon
        })
      break

  if skill_id != "" and name and color and percentage and icon and category:
    mongo.db.skills.save({
      '_id': skill_id,
      'category': category,
      'technologies': skill_arr
    })

    response = jsonify({
      'message': "Create skill",
    })

    response.status_code = 201

    return response
  
  if skill_id == "" and name and color and percentage and icon and category:
    mongo.db.skills.insert({
      'category': category,
      'technologies': [{
          'name': name,
          'color': color,
          'percentage': percentage,
          'icon': icon
        }]
    })

    response = jsonify({
      'message': "Create skill",
    })

    response.status_code = 201

    return response

  return 'Error'

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