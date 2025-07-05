from flask import Blueprint, request, jsonify
from models import Floor
from database import db

floor_bp = Blueprint('floor_bp', __name__)

@floor_bp.route('/floors', methods=['GET'])
def get_floors():
    return jsonify([{"id": f.id, "level": f.level, "name": f.name} for f in Floor.query.all()])

@floor_bp.route('/floors', methods=['POST'])
def add_floor():
    data = request.json
    floor = Floor(level=data['level'], name=data['name'])
    db.session.add(floor)
    db.session.commit()
    return jsonify({"message": "Floor added"}), 201

@floor_bp.route('/floors/<int:id>', methods=['PUT'])
def update_floor(id):
    floor = Floor.query.get_or_404(id)
    data = request.json
    floor.level = data['level']
    floor.name = data['name']
    db.session.commit()
    return jsonify({"message": "Floor updated"})

@floor_bp.route('/floors/<int:id>', methods=['DELETE'])
def delete_floor(id):
    floor = Floor.query.get_or_404(id)
    db.session.delete(floor)
    db.session.commit()
    return jsonify({"message": "Floor deleted"})
