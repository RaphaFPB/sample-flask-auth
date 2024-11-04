from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#db = SQLAlchemy(app)//A variável db vai armazenar a instância da classe SQLAlchemy
#flask shell
#db.create_all() -> criar banco de dados pelo terminal