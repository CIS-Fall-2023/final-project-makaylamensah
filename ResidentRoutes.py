from flask import Blueprint, request, jsonify
from models import Resident
from database import db

resident_bp = Blueprint('resident_bp', __name__)

@resident_bp.route('/residents', methods=['GET'])
def get_residents():
    return jsonify([{"id": r.id, "firstname": r.firstname, "lastname": r.lastname, "age": r.age, "room": r.room} for r in Resident.query.all()])

@resident_bp.route('/residents', methods=['POST'])
def add_resident():
    data = request.json
    resident = Resident(firstname=data['firstname'], lastname=data['lastname'], age=data['age'], room=data['room'])
    db.session.add(resident)
    db.session.commit()
    return jsonify({"message": "Resident added"}), 201

@resident_bp.route('/residents/<int:id>', methods=['PUT'])
def update_resident(id):
    resident = Resident.query.get_or_404(id)
    data = request.json
    resident.firstname = data['firstname']
    resident.lastname = data['lastname']
    resident.age = data['age']
    resident.room = data['room']
    db.session.commit()
    return jsonify({"message": "Resident updated"})

@resident_bp.route('/residents/<int:id>', methods=['DELETE'])
def delete_resident(id):
    resident = Resident.query.get_or_404(id)
    db.session.delete(resident)
    db.session.commit()
    return jsonify({"message": "Resident deleted"})
