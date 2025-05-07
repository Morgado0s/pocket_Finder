from flask import request, jsonify, Blueprint
from api.category.model import Category, create_category, get_category, update_category, delete_category
from flask_jwt_extended import jwt_required

blueprint = Blueprint('category', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    if not data or not all(k in data for k in ["name", "code"]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        category = create_category(data["name"], data["code"])
    except Exception as e:
        return jsonify({"error": f"Falha ao criar categoria: {str(e)}"}), 500
    return jsonify({
        "data": category.serialize(),
        "message": "Categoria criada com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    category = get_category(id)
    if category is None:
        return jsonify({"error": "Categoria não encontrada"}), 404

    return jsonify({
        "data": category.serialize(),
        "message": "Categoria recuperada com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    categories = Category.query.all()
    categories_data = [category.serialize() for category in categories]

    return jsonify({
        "data": categories_data,
        "message": "Categorias recuperadas com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        category = update_category(id, data)
        if category is None:
            return jsonify({"error": "Categoria não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar categoria: {str(e)}"}), 500

    return jsonify({
        "data": category.serialize(),
        "message": "Categoria atualizada com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        category = delete_category(id)
        if category is None:
            return jsonify({"error": "Categoria não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar categoria: {str(e)}"}), 500

    return jsonify({
        "message": "Categoria deletada com sucesso."
    }), 200 