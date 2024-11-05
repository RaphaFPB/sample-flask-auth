from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):#Model para dar base e o SQLAlchemy reconhecer como mapeavel
    #id (int), username (txt), password(text), role()txt
    id = db.Column(db.Integer, primary_key=True) #primary_key para identificar que se trata da chave principal e única que será usada para identificar o registro do usuariario na db
    username = db.Column(db.String(80), nullable = False, unique = True)#nullable = false para não permitir que insirar nomes de usuario vazio. unique = True para que usuario sja unico
    password = db.Column(db.String(80), nullable = False)
    role = db.Column(db.String(80), nullable = False, default='user')