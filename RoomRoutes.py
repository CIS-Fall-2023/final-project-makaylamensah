from flask import Blueprint, request, jsonify
from models import Room
from database import db

room_bp = Blueprint('room_bp', __name__)

@room_bp.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify([{"id": r.id, "number": r.number, "capacity": r.capacity, "floor": r.floor} for r in Room.query.all()])

@room_bp.route('/rooms', methods=['POST'])
def add_room():
    data = request.json
    room = Room(number=data['number'], capacity=data['capacity'], floor=data['floor'])
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room added"}), 201

@room_bp.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.json
    room.number = data['number']
    room.capacity = data['capacity']
    room.floor = data['floor']
    db.session.commit()
    return jsonify({"message": "Room updated"})

@room_bp.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted"})
