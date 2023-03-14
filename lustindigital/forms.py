from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lustindigital.models import Usuario

class FormLogin(FlaskForm):
    username = StringField('Digite seu usuário de acesso', validators=[DataRequired()])
    senha = PasswordField('Digite sua senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de Acesso.')
    botao_submit_login = SubmitField('Entrar')

class FormCriarConta(FlaskForm):
    username = StringField('Digite seu usuário de acesso', validators=[DataRequired()])
    email = StringField('Digite seu email', validators=[DataRequired(), Email()])
    senha = PasswordField('Digite sua senha', validators=[DataRequired(), Length(6, 20)])
    confirmar_senha = PasswordField('Digite sua senha', validators=[DataRequired(), EqualTo('senha')])
    cpf_representante = StringField('Informe um CPF', validators=[DataRequired(), Length(11)])
    client = StringField('Nome e Sobrenome', validators=[DataRequired()])
    contato = StringField('Informe um número de contato', validators=[DataRequired()])
    tipo = StringField('Tipo de serviço', validators=[DataRequired()])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado!')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Usuário já cadastrado!')