from flask import render_template, url_for, request, redirect, flash
from lustindigital import app, database, bcrypt
from lustindigital.forms import FormLogin, FormCriarConta
from lustindigital.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

@app.route('/fale-conosco')
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(username=form_login.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash('Login feito com sucesso!', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('perfil'))
        else:
            flash('Credenciais inválidas!', 'alert-danger')



    return render_template('login.html', form_login=form_login)

@app.route('/administrator', methods=['GET', 'POST'])
def criar_conta():
    form_CriarConta = FormCriarConta()

    if form_CriarConta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_CriarConta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_CriarConta.username.data, email=form_CriarConta.email.data, senha=senha_cript, cpf_representante=form_CriarConta.cpf_representante.data, client=form_CriarConta.client.data, contato=form_CriarConta.contato.data, tipo=form_CriarConta.tipo.data)
        with app.app_context():
            database.session.add(usuario)
            database.session.commit()
        flash(f'Cadastro de {form_CriarConta.username.data} realizado com sucesso!', 'alert-success')
        return redirect(url_for('login'))
    else:
        flash('Cadastro não permitido! Ou já existente', 'alert-danger')
    return render_template('administrator.html', form_CriarConta=form_CriarConta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-warning')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/post/perfil')
@login_required
def criar_post():
    return render_template('criarpost.html')
