from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
import utils

usuarios_bp = Blueprint('usuarios_bp',__name__)
from senhas import *





@usuarios_bp.route('/usuario', methods=['POST'])
def usuario():
    # Capture form data with proper validation
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    email = request.form['email']
    senha = request.form['senha']

    try:
        # Connect to the database using a context manager (recommended)
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            # Print the constructed SQL query for debugging
            sql = "INSERT INTO usuarios (nome, data_nascimento , endereco , email , senha) VALUES (%s, %s, %s, %s, %s)"
            print(f"SQL Query: {sql}")

        return jsonify({'Usuário cadastrado com sucesso!'}), 201


    except mysql.connector.Error as error:
        print(f"Failed to insert record: {error}")
        return "Ocorreu um erro ao inserir os dados.", 500


@usuarios_bp.route('/usuario/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    # Obter os dados do formulário
    dados = request.json  # Assumindo que os dados são enviados em formato JSON

    # Validar os dados
    # ... (implementar a validação aqui)

    # Construir a consulta SQL
    sql = "UPDATE usuarios SET nome=%s, email=%s, data_nascimento=%s WHERE id=%s"
    valores = (dados['nome'], dados['data_nascimento'],dados['endereco'], dados['email'], dados['senha'], usuario_id)

    # Conectar ao banco de dados e executar a consulta
    try:
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            mydb.commit()
            
            return jsonify({'': 'Usuário atualizado com sucesso'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500



@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Conectar ao banco de dados
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM usuarios"
            mycursor.execute(sql)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            usuarios = []
            for usuario in resultados:
                usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'data_nascimento': usuario[3]})

            return jsonify({'usuarios': usuarios}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500



@usuarios_bp.route('/get_usuario/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):

    try:
        # Conectar ao banco de dados
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM usuarios where id=%s "
            valores = (usuario_id,)

            mycursor.execute(sql,valores)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            usuarios = []
            for usuario in resultados:
                usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'data_nascimento': usuario[3]})

            return jsonify({'usuario': usuarios[0]}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500


@usuarios_bp.route('/get_nome_usuarios', methods=['GET'])
def get_nome_usuarios():
    nome = request.args.get('nome')

    if nome:
        # Construir a consulta SQL com o parâmetro de pesquisa
        sql = "SELECT * FROM usuarios WHERE nome LIKE %s"
        valores = ('%' + nome + '%',)
        try:
            con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500
            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                # Formatar os resultados em um JSON
                usuarios = []
                for usuario in resultados:
                    usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'data_nascimento': usuario[3]})

                return jsonify({'usuarios': usuarios}), 200
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'': 'O parâmetro "nome" é obrigatório'}), 400



@usuarios_bp.route('/del_usuario/<int:usuario_id>', methods=['DELETE'])
def del_usuario(usuario_id):
    
    try:
        # Conectar ao banco de dados
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "DELETE from usuarios where id=%s "
            valores = (usuario_id,)

            mycursor.execute(sql,valores)


            return jsonify({'usuario deletado com sucesso':  str()}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500