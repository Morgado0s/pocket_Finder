from flask import request, jsonify, Blueprint
from api.size.model import Size, create_size, get_size, update_size, delete_size
from flask_jwt_extended import jwt_required

blueprint = Blueprint('size', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()

    if not data or not all(k in data for k in ["name", "abbreviation"]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    try:
        size = create_size(data["name"], data["abbreviation"])
    except Exception as e:
        return jsonify({"error": f"Falha ao criar tamanho: {str(e)}"}), 500

    return jsonify({
        "data": size.serialize(),
        "message": "Tamanho criado com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    size = get_size(id)
    if size is None:
        return jsonify({"error": "Tamanho não encontrado"}), 404

    return jsonify({
        "data": size.serialize(),
        "message": "Tamanho recuperado com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    sizes = Size.query.all()
    sizes_data = [size.serialize() for size in sizes]

    return jsonify({
        "data": sizes_data,
        "message": "Tamanhos recuperados com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        size = update_size(id, data)
        if size is None:
            return jsonify({"error": "Tamanho não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar tamanho: {str(e)}"}), 500

    return jsonify({
        "data": size.serialize(),
        "message": "Tamanho atualizado com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        size = delete_size(id)
        if size is None:
            return jsonify({"error": "Tamanho não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar tamanho: {str(e)}"}), 500

    return jsonify({
        "message": "Tamanho deletado com sucesso."
    }), 200 