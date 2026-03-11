from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password') 

  if not username or not password:
    return jsonify({'message': 'Credenciais inválidas'}), 400
  
  user = User.query.filter_by(username=username).first()

  if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
    login_user(user)
    return jsonify({'message': 'Login bem sucedido'})
  return jsonify({'message': 'Credenciais inválidas'}), 400
    

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logout bem sucedido'})

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if not username or not password:
    return jsonify({'message': 'Dados inválidos'}), 400
  
  if User.query.filter_by(username=username).first():
    return jsonify({'message': 'Usuário já cadastrado'}), 400

  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  new_user = User(username=username, password=hashed_password.decode('utf-8'), role='user')
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'Uusuário criado com sucesso'})


@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def get_user(id_user):
  user = User.query.get(id_user)

  if not user:
    return jsonify({'message': 'Usuário não encontrado'}), 404

  if user:
    return {'username': user.username}
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    user = User.query.get(id_user)

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    data = request.json
    new_password = data.get('password')

    # Verifica se a nova senha, quando criptografada, seria igual à atual
    if bcrypt.checkpw(new_password.encode('utf-8'), user.password.encode('utf-8')):
      return jsonify({'message': 'Mesma senha fornecida anteriormente'}), 400

    if id_user != current_user.id and current_user.role == 'user':
      return jsonify({'message': 'Operação não permitida'}), 403

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')

    db.session.commit()
    return jsonify({'message': f'Usuário {user.username} atualizado com sucesso'})
  
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if not user:
    return jsonify({'message': 'Usuário não encontrado'}), 404
  
  if user.id == current_user.id:
    return jsonify({'message': 'Não é permitido deletar o próprio usuário'}), 403
  
  if current_user.role != 'admin':
    return jsonify({'message': 'Operação não permitida'}), 403
  
  db.session.delete(user)
  db.session.commit()
  return jsonify({'message': f'Usuário {user.username} deletado com sucesso'})


@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'Hello World!'

if __name__=='__main__':
  app.run(debug=True)