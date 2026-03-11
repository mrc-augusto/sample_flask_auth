from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

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

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
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

  if username and password:
    if User.query.filter_by(username=username).first():
      return jsonify({'message': 'Usuário já cadastrado'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Uusuário criado com sucesso'})
  
  return jsonify({'message': 'Dados inválidos'}), 400

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

  if new_password == user.password:
    return jsonify({'message': 'Mesma senha fornecida anteriormente'}), 400
  
  user.password = new_password

  db.session.commit()
  return jsonify({'message': f'Usuário {user.username} atualizado com sucesso'})  
  

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if not user:
    return jsonify({'message': 'Usuário não encontrado'}), 404
  
  if user.id == current_user.id:
    return jsonify({'message': 'Não é permitido deletar o próprio usuário'}), 400
  
  db.session.delete(user)
  db.session.commit()
  return jsonify({'message': f'Usuário {user.username} deletado com sucesso'})




@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'Hello World!'

if __name__=='__main__':
  app.run(debug=True)