from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dados import Autor, Postagem, app, db
import json
import jwt
from datetime import datetime, timedelta

# Rota Login
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or auth.username or not auth.password:
        return  make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token})
    return  make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório'})



# Rota padrão - GET https://localhost:5000
@app.route('/')
def obter_postagens():
    postagens = Postagem.query.all()

    list_postagens = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        list_postagens.append(postagem_atual)
    return jsonify({'postagens': list_postagens})

# Obter postagem por id - GET https://localhost:5000/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['GET'])
def obter_postagem_por_indice(id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor

    return jsonify({'postagens': postagem_atual})

# Criar uma nova postagem - POST https://localhost:5000/postagem
@app.route('/postagem', methods=['POST'])
def nova_postagem():
    nova_postagem = request.get_json()
    postagem = Postagem(
        titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])

    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso'})

# Alterar uma postagem existente - PUT https://localhost:5000/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
def alterar_postagem(id_postagem):
    postagem_alterada = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = postagem_alterada['titulo']
    except:
        pass
    try:
        postagem.id_autor = postagem_alterada['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucessso'})

# Excluir uma postagem - DELETE - https://localhost:5000/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
def excluir_postagem(id_postagem):
    postagem_a_ser_excluida = Postagem.query.filter_by(
        id_postagem=id_postagem).first()
    if not postagem_a_ser_excluida:
        return jsonify({'mensagem': 'Não foi encontrado uma postagem com este id'})
    db.session.delete(postagem_a_ser_excluida)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem excluída com sucesso!'})


# API autores
@app.route('/autores')
def obter_autores():
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})
    


@app.route('/autores/<int:id_autor>', methods=['GET'])
def obter_autor_por_id(id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Autor não encontrado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify(f'Você buscou pelo autor: {autor_atual}')


@app.route('/autores', methods=['POST'])
def novo_autor():
    print('deu erro')
    novo_autor = request.get_json()
    autor = Autor(
        nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email']
    )
    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Usuario criado com sucessso'}, 200)


@app.route('/autores/<int:id_autor>', methods=['PUT'])
def alterar_autor(id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem': 'Este usuario não foi encontrado'})
    try:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass

    db.session.commit()
    return jsonify({'mesagem': 'Usuario alterado com sucesso'})


@app.route('/autores/<int:id_autor>', methods=['DELETE'])
def excluir_autor(id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'mensagem': 'O autor não foi encontrado!'})
    db.session.delete(autor_existente)
    db.session.commit()

    return jsonify({'mensagem': 'O autor foi excluído com sucesso!'})


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
