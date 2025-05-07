from flask import request, jsonify, Blueprint
from api.gender.model import Gender, create_gender, get_gender, update_gender, delete_gender
from flask_jwt_extended import jwt_required

blueprint = Blueprint('gender', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    if not data or not all(k in data for k in ["name", "abbreviation"]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        gender = create_gender(data["name"], data["abbreviation"])
    except Exception as e:
        return jsonify({"error": f"Falha ao criar gênero: {str(e)}"}), 500
    return jsonify({
        "data": gender.serialize(),
        "message": "Gênero criado com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    gender = get_gender(id)
    if gender is None:
        return jsonify({"error": "Gênero não encontrado"}), 404

    return jsonify({
        "data": gender.serialize(),
        "message": "Gênero recuperado com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    genders = Gender.query.all()
    genders_data = [gender.serialize() for gender in genders]

    return jsonify({
        "data": genders_data,
        "message": "Gêneros recuperados com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        gender = update_gender(id, data)
        if gender is None:
            return jsonify({"error": "Gênero não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar gênero: {str(e)}"}), 500

    return jsonify({
        "data": gender.serialize(),
        "message": "Gênero atualizado com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        gender = delete_gender(id)
        if gender is None:
            return jsonify({"error": "Gênero não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar gênero: {str(e)}"}), 500

    return jsonify({
        "message": "Gênero deletado com sucesso."
    }), 200 