from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criar uma api flask
app = Flask(__name__)

# Criar uma instancia de SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323f#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db:SQLAlchemy

# Definir a estrutura da tabela Postagem - id_postagem, titulo, autor
class Postagem(db.Model):
    # Estrutura
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    # Relacionamento da tabela postagem com a do autor
    id_autor = db.Column(db.Integer,db.ForeignKey('autor.id_autor'))

# Definir a estrutura da tabela Autor - id_autor, nome, email, senha, admin, postagens
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    # relacionamento da tabela autor com a postagem
    postagens = db.relationship('Postagem')

def inicializar_banco():
    with app.app_context():
        # Executar o comando para criar o banco de dados
        # Apaga qualquer estrutura previa e rodar apenas uma vez
        db.drop_all()
        # criar a estrutura inicial
        db.create_all()

        # Criando usuarios administradores
        autor = Autor(nome='glauber',email='glauber@gmail.com',senha='123456',admin=True)
        db.session.add(autor)
        db.session.commit()

if __name__=="__main__":
    inicializar_banco()