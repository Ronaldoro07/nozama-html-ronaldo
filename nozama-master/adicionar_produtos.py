from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'nozama'


@app.route('/lojas', methods=['POST'])
def criar_lojas():
    nome=request.form['nome']
    cod_do_produto=request.form['cod_do_produto']
    preco_do_produto=request.form['preco_do_produto']
    descricao_do_produto=request.form['descricao_do_produto']
    


    try:
            connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
            )
            cursor = connection.cursor()

            
            sql = "INSERT INTO lojas (nome  , cod_do_produto , preco_do_produto , descricao_do_produto) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql , (nome , cod_do_produto , preco_do_produto , descricao_do_produto))
            connection.commit()
    except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return "Erro ao processar os dados. Tente novamente mais tarde."
    finally:
            
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

        
            return redirect(url_for('sucesso'))    

@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'



if __name__ == '__main__':
    app.run(debug=True)