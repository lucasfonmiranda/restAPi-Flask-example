from flask import Flask, jsonify, abort, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)    

class Develpor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Strig(20))
	hireDate = db.Column(db.date)
	focus = db.Column(db.Strig(50))

	def __init__(self, name, hireDate, focus):
		self.name = name
		self.hireDate = datetime.datetime.strptime(hireDate, "%d%m%Y").date()
		self.focus = focus 

@app.route('/dev/', methods= ['GET'])
def index():
	return jsonify({'developers ': Developer.query.all()})		

@app.route('/dev/', methods= ['POST'])
def create_dev():
	if not request.json or not 'name' in request.json:
		abort(400)
	dev = Developer(request.json.name, request.json.get('hireDate', ''), request.json.get('focus', ''))
	db.session.add(dev)
	db.session.commit()
	return jsonify({'developer ': dev}), 201

@app.route('/dev/<int:id>/')
def get_dev(id):
	return jsonify({'developer: ', Developer.query.get(id)})

@app.route('/dev/<int:id>/', methods=['DELETE'])
def delete_dev(id):
	db.session.delete(User.query.get(id))
	db.session.commit()
	return jsonify({'result ': True})

@app.route('/dev/<int:id>/', methods=['PUT'])
def update_dev(id):
	dev = Developer.query.get(id)
	dev.name = request.json.get('name', dev.name)
	dev.hireDate = request.json.get('hireDate', dev.name)
	dev.focus = request.json.get('focus', dev.focus)
	db.session.commit()
	return jsonify({'dev': dev})