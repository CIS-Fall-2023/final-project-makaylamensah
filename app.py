from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config - replace with your actual credentials
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://admin:Youngkayla35!@cis2368spring.cqvqcae80duk.us-east-1.rds.amazonaws.com/cis2368springdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Floor(db.Model):
    __tablename__ = 'floor'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)

class Resident(db.Model):
    __tablename__ = 'resident'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

# Simple in-memory login credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Floor CRUD endpoints
@app.route('/floors', methods=['GET'])
def get_floors():
    floors = Floor.query.all()
    return jsonify([{"id": f.id, "level": f.level, "name": f.name} for f in floors])

@app.route('/floors', methods=['POST'])
def add_floor():
    data = request.json
    new_floor = Floor(level=data['level'], name=data['name'])
    db.session.add(new_floor)
    db.session.commit()
    return jsonify({"message": "Floor added", "id": new_floor.id}), 201

@app.route('/floors/<int:id>', methods=['PUT'])
def update_floor(id):
    floor = Floor.query.get_or_404(id)
    data = request.json
    floor.level = data.get('level', floor.level)
    floor.name = data.get('name', floor.name)
    db.session.commit()
    return jsonify({"message": "Floor updated"})

@app.route('/floors/<int:id>', methods=['DELETE'])
def delete_floor(id):
    floor = Floor.query.get_or_404(id)
    db.session.delete(floor)
    db.session.commit()
    return jsonify({"message": "Floor deleted"})

# Room CRUD endpoints
@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{"id": r.id, "capacity": r.capacity, "number": r.number, "floor": r.floor} for r in rooms])

@app.route('/rooms', methods=['POST'])
def add_room():
    data = request.json
    new_room = Room(capacity=data['capacity'], number=data['number'], floor=data['floor'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Room added", "id": new_room.id}), 201

@app.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.json
    room.capacity = data.get('capacity', room.capacity)
    room.number = data.get('number', room.number)
    room.floor = data.get('floor', room.floor)
    db.session.commit()
    return jsonify({"message": "Room updated"})

@app.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted"})

# Resident CRUD endpoints
@app.route('/residents', methods=['GET'])
def get_residents():
    residents = Resident.query.all()
    return jsonify([{
        "id": r.id,
        "firstname": r.firstname,
        "lastname": r.lastname,
        "age": r.age,
        "room": r.room
    } for r in residents])

@app.route('/residents', methods=['POST'])
def add_resident():
    data = request.json
    new_resident = Resident(
        firstname=data['firstname'],
        lastname=data['lastname'],
        age=data['age'],
        room=data['room']
    )
    db.session.add(new_resident)
    db.session.commit()
    return jsonify({"message": "Resident added", "id": new_resident.id}), 201

@app.route('/residents/<int:id>', methods=['PUT'])
def update_resident(id):
    resident = Resident.query.get_or_404(id)
    data = request.json
    resident.firstname = data.get('firstname', resident.firstname)
    resident.lastname = data.get('lastname', resident.lastname)
    resident.age = data.get('age', resident.age)
    resident.room = data.get('room', resident.room)
    db.session.commit()
    return jsonify({"message": "Resident updated"})

@app.route('/residents/<int:id>', methods=['DELETE'])
def delete_resident(id):
    resident = Resident.query.get_or_404(id)
    db.session.delete(resident)
    db.session.commit()
    return jsonify({"message": "Resident deleted"})

# Create tables and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/')
def home():
    return "Senior Citizen Facility API is running!"
