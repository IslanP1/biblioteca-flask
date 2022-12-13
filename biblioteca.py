from flask import Flask, render_template, request, redirect, session, flash, url_for


class Livro:
    def __init__(self, nome, genero, autor):
        self.nome = nome
        self.genero = genero
        self.autor = autor

    def __str__(self):
        return self.nome


livro1 = Livro('A moreninha', 'Romance', 'Joaquim Manuel de Macedo')
livro2 = Livro('As crônicas de Nárnia', 'Fantasia', 'C. S. Lewis')
livro3 = Livro('Iracema', 'Romance', 'José de Alencar')
lista = [livro1, livro2, livro3]

app = Flask(__name__)
app.secret_key = 'ifpb2022'


@app.route('/')
def index():
    return render_template('lista.html', titulo='livros', livros=lista)


@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=cadastro')
    return render_template('cadastro.html', titulo='Novo Livro')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    autor = request.form['autor']
    livro = Livro(nome, genero, autor)
    lista.append(livro)
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
       return redirect('/{}'.format(proxima_pagina))
   else:
       flash('Senha ou usuário incorreto!')
       return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


app.run(debug=True)
