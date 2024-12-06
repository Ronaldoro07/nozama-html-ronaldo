
from flask import Flask, flash, render_template, request, redirect, url_for
import mysql.connector
from utils import *

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'trab_final'

@app.route('/', methods=['GET'])
def inicial() :
      return render_template('/cadastro_usuario.html')

@app.route('/create_usuario', methods=['POST'])
def criar_usuario():

    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    email = request.form['email']
    senha = request.form['senha']

    try :
        connection = connect_to_database()
            
        cursor = connection.cursor()

        # Executar comando SQL para inserir dados
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nome = %s", (nome,))
        count = cursor.fetchone()[0]  # Obtém o primeiro valor da primeira linha do resultado

        
        sql = "INSERT INTO usuarios (nome , endereco , email , senha , data_nascimento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql , (nome , endereco , email , senha, data_nascimento))
        connection.commit()
        # Redirecionar para página de sucesso ou outra página
        return redirect(url_for('sucesso')) 

    except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return redirect(url_for('ERRO OS DADOS NAO FORAM INSERIDOS'))
    finally:
            # Fechar conexão com o banco de dados
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

           
# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'



if __name__ == '__main__':
    app.run(debug=True)