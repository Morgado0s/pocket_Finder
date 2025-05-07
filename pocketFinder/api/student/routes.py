from flask import request, jsonify, Blueprint
from api.student.model import Student, create_student, get_student, update_student, delete_student
from flask_jwt_extended import jwt_required

blueprint = Blueprint('student', __name__)

@blueprint.route("/create", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    required = ["name", "product_id", "room_id", "admin_id"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        student = create_student(
            data["name"],
            data["product_id"],
            data["room_id"],
            data["admin_id"]
        )
    except Exception as e:
        return jsonify({"error": f"Falha ao criar aluno: {str(e)}"}), 500
    return jsonify({
        "data": student.serialize(),
        "message": "Aluno criado com sucesso."
    }), 201

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    student = get_student(id)
    if student is None:
        return jsonify({"error": "Aluno não encontrado"}), 404

    return jsonify({
        "data": student.serialize(),
        "message": "Aluno recuperado com sucesso."
    }), 200

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    students = Student.query.all()
    students_data = [student.serialize() for student in students]

    return jsonify({
        "data": students_data,
        "message": "Alunos recuperados com sucesso."
    }), 200

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()

    try:
        student = update_student(id, data)
        if student is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar aluno: {str(e)}"}), 500

    return jsonify({
        "data": student.serialize(),
        "message": "Aluno atualizado com sucesso."
    }), 200

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        student = delete_student(id)
        if student is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Falha ao deletar aluno: {str(e)}"}), 500

    return jsonify({
        "message": "Aluno deletado com sucesso."
    }), 200 