from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_muito_forte_aqui'  # MUDE ISSO!

# Simulação de banco de dados (em produção use SQLAlchemy + banco real)
USUARIOS = {
    "admin": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
    "usuario": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
}

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página.'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in USUARIOS:
        return User(username)
    return None

# Formulário de Login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode()

        # Verifica se usuário existe
        if username in USUARIOS:
            hashed = USUARIOS[username].encode()
            if bcrypt.checkpw(password, hashed):
                user = User(username)
                login_user(user)
                flash(f'Bem-vindo, {username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Senha incorreta!', 'danger')
        else:
            flash('Usuário não encontrado!', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
