from flask import request, jsonify, Blueprint
from api.product.model import Product, create_product, get_product, update_product, delete_product
from flask_jwt_extended import jwt_required

blueprint = Blueprint('product', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    required = ["name", "description", "category_id", "size_id", "gender_id", "room_id"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        product = create_product(
            data["name"],
            data["description"],
            data["category_id"],
            data["size_id"],
            data["gender_id"],
            data["room_id"]
        )
    except Exception as e:
        return jsonify({"error": f"Falha ao criar produto: {str(e)}"}), 500
    return jsonify({
        "data": product.serialize(),
        "message": "Produto criado com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    product = get_product(id)
    if product is None:
        return jsonify({"error": "Produto não encontrado"}), 404

    return jsonify({
        "data": product.serialize(),
        "message": "Produto recuperado com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    products = Product.query.all()
    products_data = [product.serialize() for product in products]

    return jsonify({
        "data": products_data,
        "message": "Produtos recuperados com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        product = update_product(id, data)
        if product is None:
            return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar produto: {str(e)}"}), 500

    return jsonify({
        "data": product.serialize(),
        "message": "Produto atualizado com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        product = delete_product(id)
        if product is None:
            return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar produto: {str(e)}"}), 500

    return jsonify({
        "message": "Produto deletado com sucesso."
    }), 200 