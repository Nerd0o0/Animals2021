from flask import Flask
from flask import request
from flasgger import Swagger

# просто чтобы обойти ограничения colab - чтобы иметь возможность постучаться извне
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
run_with_ngrok(app)
swagger = Swagger(app, template_file='swag.yaml')

class Animal:
  name = ''
  kind = ''

  def __init__(self, name, kind):
    self.name = name
    self.kind = kind
animals = [Animal("Romashka", "Rabit"), Animal("Rodger","Rabit")]

from flask_marshmallow import Marshmallow
from marshmallow import fields
ma = Marshmallow(app)

class AnimalSchema(ma.Schema):
  name = fields.String()
  kind = fields.String()

@app.route('/')
def hello_world():
  result = "<div style='background: aqua;'><h1 style='color: green;background: yellow;'>Hello world</h1> <div>"
  for elem in animals:
    result += "<div> <b>" + elem.name + "</b> <i>" + elem.kind + "</i></div>"
  result += "</div></div>"
  return result

@app.route('/animals')
def get_animals():
  return AnimalSchema(many=True).dumps(animals)

@app.route('/animals', methods=['POST'])
def add_animal():
  ###############
  if request.json.get('name') == '' or request.json.get('kind') == '':
    return {"message": "Name is required"}, 400
  ###############
  animal = Animal(request.json.get('name'), request.json.get('kind'))
  animals.append(animal)
  return AnimalSchema().dumps(animal)

@app.route('/animal/<string:name>')
def get_by_name(name):
  for elem in animals:
    if elem.name == name:
      return AnimalSchema().dumps(elem)
  return {"message": "Not found"}, 404

@app.route('/animal/<string:name>', methods=['DELETE'])
def delete_by_name(name):
  ###############
  for elem in animals:
    if elem.name == name:
      animals.remove(elem)
      return AnimalSchema().dumps(elem)
  
  return {"message": "Not found"}, 404
  ###############

@app.route('/animal/<string:name>', methods=['PATCH'])
def patch_by_name(name):
  ###############
  for elem in animals:
    if elem.name == name:
      elem.name = request.json.get('name')
      elem.kind = request.json.get('kind')
      return AnimalSchema().dumps(elem)
  
  return {"message": "Not found"}, 404
  ###############

app.run()
