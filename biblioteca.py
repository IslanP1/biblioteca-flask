from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ifpb2022'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD='postgresql',
    usuario='postgres',
    senha='123456',
    servidor='localhost',
    database='biblioteca-flask'
)

db = SQLAlchemy(app)

class Livros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    num_paginas = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome


@app.route('/')
def index():
    lista = Livros.query.order_by(Livros.id)
    return render_template('lista.html', titulo='livros', livros=lista)


@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('login', proxima=url_for("cadastro"))
    return render_template('cadastro.html', titulo='Novo Livro')


@app.route('/criar', methods=['POST',])
def criar():
   nome = request.form['nome']
   genero = request.form['genero']
   autor = request.form['autor']
   num_paginas = request.form['num_paginas']

   livro = Livros.query.filter_by(nome=nome).first()

   if livro:
       flash('Livro já existente!')
       return redirect(url_for('index'))

   novo_livro = Livros(nome=nome, genero=genero, autor=autor, num_paginas=num_paginas)

   db.session.add(novo_livro)
   db.session.commit()

   flash('Livro criado com sucesso!')
   return redirect(url_for('index'))




@app.route('/login')
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", titulo="Login", proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if '12345' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        proxima_pagina = request.form['proxima']
        flash(request.form['usuario'] + ' logou com sucesso!')
        return redirect(proxima_pagina)
    else:
        flash('Senha ou usuário incorreto!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


app.run(debug=True)
