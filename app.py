import random
import datetime
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


app = Flask(__name__)

# CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:lamotte@localhost:5432/tukki"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'  # Change in production

db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# UTILS
def generate_code():
    return f"{random.randint(1000, 9999)}"

def generate_token(user):
    payload = {
        'user_id': user.id,
        'phone': user.phone,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# ROUTES

# 1. Demander le code
@app.route('/auth/request-code', methods=['POST'])
def request_code():
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    code = generate_code()
    new_code = Code(phone=phone, code=code)
    db.session.add(new_code)
    db.session.commit()

    print(f"[SMS] Code for {phone}: {code}")
    return jsonify({"message": "Code sent"}), 200

# 2. Vérifier le code
@app.route('/auth/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')

    if not phone or not code:
        return jsonify({"error": "Phone and code are required"}), 400

    last_code = Code.query.filter_by(phone=phone, code=code).order_by(Code.created_at.desc()).first()

    if not last_code:
        return jsonify({"error": "Invalid code"}), 400
    user = User.query.filter_by(phone=phone).first()
    if user:
        token = generate_token(user)
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
    else:
        return jsonify({"message": "User not registered"}), 200

# 3. Enregistrer un nouveau user
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not phone or not first_name or not last_name:
        return jsonify({"error": "Missing fields"}), 400

    existing = User.query.filter_by(phone=phone).first()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(phone=phone, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user)
    return jsonify({
        "token": token,
        "user": {
            "id": new_user.id,
            "phone": new_user.phone,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }), 201


def create_tables():
    db.create_all()

@app.route('/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        "user": {
            "id": current_user.id,
            "phone": current_user.phone,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name
        }
    }), 200


if __name__ == '__main__':
    # with app.app_context():
    #     create_tables()
    app.run(debug=True)
