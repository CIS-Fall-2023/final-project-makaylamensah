from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# -------------------------------------------------
# Flask app setup
# -------------------------------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")

# -------------------------------------------------
# Database config (your RDS)
# -------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://admin:Youngkayla35!@cis2368spring.cqvqcae80duk.us-east-1.rds.amazonaws.com/cis2368springdb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------
# Models
# -------------------------------------------------
class Floor(db.Model):
    __tablename__ = "floor"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "level": self.level, "name": self.name}


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, db.ForeignKey("floor.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "number": self.number,
            "floor": self.floor,
        }


class Resident(db.Model):
    __tablename__ = "resident"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "age": self.age,
            "room": self.room,
        }

# -------------------------------------------------
# Simple in-memory login
# -------------------------------------------------
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def _extract_credentials(req):
    if req.is_json:
        data = req.get_json(silent=True) or {}
        return data.get("username", ""), data.get("password", "")
    return req.form.get("username", ""), req.form.get("password", "")

# -------------------------------------------------
# UI routes (templates)  — keep these ONLY for pages
# -------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("index.html")

@app.route("/floors", methods=["GET"])
def floors_page():
    return render_template("floors.html")

@app.route("/rooms", methods=["GET"])
def rooms_page():
    return render_template("rooms.html")

@app.route("/residents", methods=["GET"])
def residents_page():
    return render_template("residents.html")

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# -------------------------------------------------
# API routes (prefix: /api) — JSON ONLY
# -------------------------------------------------

# ---- LOGIN ----
@app.route("/api/login", methods=["POST"])
@app.route("/login", methods=["POST"])  # also accept plain form posts
def api_login():
    username, password = _extract_credentials(request)
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ---- FLOORS ----
@app.route("/api/floors", methods=["GET"])
def api_get_floors():
    floors = Floor.query.order_by(Floor.level.asc()).all()
    return jsonify([f.to_dict() for f in floors]), 200

@app.route("/api/floors", methods=["POST"])
def api_add_floor():
    data = request.get_json(silent=True) or {}
    level = data.get("level")
    name = data.get("name")
    if level is None or name is None:
        return jsonify({"error": "Missing 'level' or 'name'"}), 400
    new_floor = Floor(level=int(level), name=str(name))
    db.session.add(new_floor)
    db.session.commit()
    return jsonify({"message": "Floor added", "id": new_floor.id}), 201

@app.route("/api/floors/<int:floor_id>", methods=["PUT"])
def api_update_floor(floor_id):
    floor = Floor.query.get_or_404(floor_id)
    data = request.get_json(silent=True) or {}
    if "level" in data:
        floor.level = int(data["level"])
    if "name" in data:
        floor.name = str(data["name"])
    db.session.commit()
    return jsonify({"message": "Floor updated"}), 200

@app.route("/api/floors/<int:floor_id>", methods=["DELETE"])
def api_delete_floor(floor_id):
    floor = Floor.query.get_or_404(floor_id)
    db.session.delete(floor)
    db.session.commit()
    return jsonify({"message": "Floor deleted"}), 200

# ---- ROOMS ----
@app.route("/api/rooms", methods=["GET"])
def api_get_rooms():
    rooms = Room.query.order_by(Room.number.asc()).all()
    return jsonify([r.to_dict() for r in rooms]), 200

@app.route("/api/rooms", methods=["POST"])
def api_add_room():
    data = request.get_json(silent=True) or {}
    capacity = data.get("capacity")
    number = data.get("number")
    floor_fk = data.get("floor")
    if capacity is None or number is None or floor_fk is None:
        return jsonify({"error": "Missing 'capacity', 'number', or 'floor'"}), 400
    new_room = Room(capacity=int(capacity), number=int(number), floor=int(floor_fk))
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Room added", "id": new_room.id}), 201

@app.route("/api/rooms/<int:room_id>", methods=["PUT"])
def api_update_room(room_id):
    room = Room.query.get_or_404(room_id)
    data = request.get_json(silent=True) or {}
    if "capacity" in data: room.capacity = int(data["capacity"])
    if "number" in data:   room.number   = int(data["number"])
    if "floor" in data:    room.floor    = int(data["floor"])
    db.session.commit()
    return jsonify({"message": "Room updated"}), 200

@app.route("/api/rooms/<int:room_id>", methods=["DELETE"])
def api_delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted"}), 200

# ---- RESIDENTS ----
@app.route("/api/residents", methods=["GET"])
def api_get_residents():
    residents = Resident.query.order_by(Resident.lastname.asc(), Resident.firstname.asc()).all()
    out = []
    for r in residents:
        out.append({
            "id": r.id,
            "firstname": r.firstname,
            "lastname": r.lastname,
            "age": r.age,
            "room": int(r.room) if isinstance(r.room, int) else getattr(r.room, "id", r.room),
        })
    return jsonify(out), 200

@app.route("/api/residents", methods=["POST"])
def api_add_resident():
    data = request.get_json(silent=True) or {}
    try:
        res = Resident(
            firstname=str(data["firstname"]),
            lastname=str(data["lastname"]),
            age=int(data["age"]),
            room=int(data["room"]),
        )
        db.session.add(res)
        db.session.commit()
        return jsonify({"message": "Resident added", "id": res.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/api/residents/<int:resident_id>", methods=["PUT"])
def api_update_resident(resident_id):
    r = Resident.query.get_or_404(resident_id)
    data = request.get_json(silent=True) or {}
    try:
        if "firstname" in data: r.firstname = str(data["firstname"])
        if "lastname"  in data: r.lastname  = str(data["lastname"])
        if "age"       in data: r.age       = int(data["age"])
        if "room"      in data: r.room      = int(data["room"])
        db.session.commit()
        return jsonify({"message": "Resident updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/api/residents/<int:resident_id>", methods=["DELETE"])
def api_delete_resident(resident_id):
    r = Resident.query.get_or_404(resident_id)
    try:
        db.session.delete(r)
        db.session.commit()
        return jsonify({"message": "Resident deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# -------------------------------------------------
# Bootstrap
# -------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # app.run(debug=True, port=5001)  # use a different port if 5000 is busy
    app.run(debug=True)
