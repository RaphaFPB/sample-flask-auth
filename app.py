from flask import Flask,request,jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user,login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"



login_manager = LoginManager()
db.init_app(app)#apos de fazer tudo, iniciar database no app
login_manager.init_app(app)
#view login
login_manager.login_view='login'
#Session -> conexão ativa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)#busca do user na db

@app.route('/login', methods=["POST"])
def login():
    """CREDENCIAIS RECEBIDAS"""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    """TEMOS USERNAME E PASSWORD?"""
    if username and password: 
        #login
        user = User.query.filter_by(username=username).first()#para acessar a base usando filter() (Pois não é uma chave primária), e usando first para retornar apenas um registro(o primeiro nome) e não uma lista
        #encontrei user? and...a senha do user é igual a senha q recebi?
        if user and user.password == password:
            login_user(user)#AUTENTICAÇÃO DO USER
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route("/logout", methods=["GET"])
@login_required#protege a rota de usuarios que requisitarem essa rota sem estar logado
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})
    

@app.route('/user', methods=["POST"])
#@login_required#cadastrar somente se estiver autenticado
def create_user():
    data = request.json
    username= data.get("username")
    password= data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)


    if user:
        return {"username": user.username}#retorna username
    
    return jsonify({"message": "Usuario não encontrado"}),404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data =request.json
    user = User.query.get(id_user)

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()#n é necessario sessio.add pois não será adicioonado nada, estamos apenas alterando

        return jsonify({"message": f"Usuario {id_user} atualizado com sucesso"})

    return jsonify({"message": "Usuario não encontrado"}),404

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})
    
    return jsonify({"message": "Usuario não encontrado"}),404


if __name__=='__main__':
    app.run(debug=True)