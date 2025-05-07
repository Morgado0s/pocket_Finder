from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/pocketfinder')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações do JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Inicialização das extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importação e registro dos blueprints
from api.admin.routes import blueprint as admin_blueprint
from api.student.routes import blueprint as student_blueprint
from api.product.routes import blueprint as product_blueprint
from api.category.routes import blueprint as category_blueprint
from api.size.routes import blueprint as size_blueprint
from api.gender.routes import blueprint as gender_blueprint
from api.room.routes import blueprint as room_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
app.register_blueprint(student_blueprint, url_prefix='/api/student')
app.register_blueprint(product_blueprint, url_prefix='/api/product')
app.register_blueprint(category_blueprint, url_prefix='/api/category')
app.register_blueprint(size_blueprint, url_prefix='/api/size')
app.register_blueprint(gender_blueprint, url_prefix='/api/gender')
app.register_blueprint(room_blueprint, url_prefix='/api/room')

if __name__ == '__main__':
    app.run(debug=True) 