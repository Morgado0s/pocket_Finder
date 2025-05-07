from flask import request, jsonify, Blueprint
from api.admin.model import Admin, create_admin, get_admin, update_admin, delete_admin, get_admin_by_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

blueprint = Blueprint('admin', __name__)

@blueprint.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        
        # Verificar campos obrigatórios
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Buscar admin pelo email
        admin = get_admin_by_email(data['email'])
        if not admin:
            return jsonify({'error': 'Admin não encontrado'}), 404
        
        # Verificar senha
        if not admin.check_password(data['password']):
            return jsonify({'error': 'Senha incorreta'}), 401
        
        # Gerar token JWT
        access_token = create_access_token(identity=str(admin.id))
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route("/create", methods=["POST"])
def create():
    try:
        data = request.get_json()
        
        # Verificar campos obrigatórios
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Criar admin
        admin = create_admin(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'message': 'Admin criado com sucesso',
            'admin': admin.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route("/read/<int:id>", methods=["GET"])
@jwt_required()
def read(id):
    try:
        admin = get_admin(id)
        if not admin:
            return jsonify({'error': 'Admin não encontrado'}), 404
        
        return jsonify(admin.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route("/read/all", methods=["GET"])
@jwt_required()
def read_all():
    try:
        admins = Admin.query.all()
        return jsonify([admin.to_dict() for admin in admins]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    try:
        data = request.get_json()
        admin = update_admin(id, data)
        
        if not admin:
            return jsonify({'error': 'Admin não encontrado'}), 404
        
        return jsonify({
            'message': 'Admin atualizado com sucesso',
            'admin': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        if delete_admin(id):
            return jsonify({'message': 'Admin excluído com sucesso'}), 200
        return jsonify({'error': 'Admin não encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400 