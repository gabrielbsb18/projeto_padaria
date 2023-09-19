import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuração da conexão com o banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "bdecomerce",
}

# Conectando ao banco de dados
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Criação da tabela de estoque se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INT AUTO_INCREMENT PRIMARY KEY,
        produto VARCHAR(255),
        quantidade INT
    )
''')
conn.commit()


@app.route('/')
def index():
    cursor.execute('SELECT produto, quantidade FROM estoque')
    estoque = cursor.fetchall()
    return render_template('index.html', estoque=estoque)


@app.route('/adicionar', methods=['POST'])
def adicionar_estoque():
    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])

    cursor.execute('INSERT INTO estoque (produto, quantidade) VALUES (%s, %s)', (produto, quantidade))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/pedido', methods=['POST'])
def fazer_pedido():
    produto_pedido = request.form['produto_pedido']
    quantidade_pedido = int(request.form['quantidade_pedido'])

    cursor.execute('SELECT quantidade FROM estoque WHERE produto = %s', (produto_pedido,))
    estoque_atual = cursor.fetchone()

    if estoque_atual:
        estoque_atual = estoque_atual[0]

        if quantidade_pedido <= estoque_atual:
            nova_quantidade = estoque_atual - quantidade_pedido
            cursor.execute('UPDATE estoque SET quantidade = %s WHERE produto = %s', (nova_quantidade, produto_pedido))
            conn.commit()
            return redirect(url_for('index'))
        else:
            return "Quantidade insuficiente em estoque para atender ao pedido."
    else:
        return "Produto não encontrado no estoque."


if __name__ == '__main__':
    app.run(debug=True)
