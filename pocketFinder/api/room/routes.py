from flask import request, jsonify, Blueprint
from api.room.model import Room, create_room, get_room, update_room, delete_room
from flask_jwt_extended import jwt_required

blueprint = Blueprint('room', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    if not data or not all(k in data for k in ["name", "shift"]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        room = create_room(data["name"], data["shift"])
    except Exception as e:
        return jsonify({"error": f"Falha ao criar sala: {str(e)}"}), 500
    return jsonify({
        "data": room.serialize(),
        "message": "Sala criada com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    room = get_room(id)
    if room is None:
        return jsonify({"error": "Sala não encontrada"}), 404

    return jsonify({
        "data": room.serialize(),
        "message": "Sala recuperada com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    rooms = Room.query.all()
    rooms_data = [room.serialize() for room in rooms]

    return jsonify({
        "data": rooms_data,
        "message": "Salas recuperadas com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        room = update_room(id, data)
        if room is None:
            return jsonify({"error": "Sala não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar sala: {str(e)}"}), 500

    return jsonify({
        "data": room.serialize(),
        "message": "Sala atualizada com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        room = delete_room(id)
        if room is None:
            return jsonify({"error": "Sala não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar sala: {str(e)}"}), 500

    return jsonify({
        "message": "Sala deletada com sucesso."
    }), 200 