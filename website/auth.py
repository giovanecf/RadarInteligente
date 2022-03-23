from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta.', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print("POST")
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('\'Email\' já existe.', category='error')
            print("Existe")
        elif len(email) < 4:
            flash('\'Email\' precisa ser maior que 3 caracteres.', category='error')
            print("Maior")
        elif len(name) < 2:
            flash('\'Nome\' precisa ter mais de uma letra.', category='error')
            print("MENOS UM")
        elif password1 != password2:
            flash('\'Senhas\' são diferentes.', category='error')
            print("Diferentes")
        elif len(password1) < 7:
            flash('\'Senha\' precisa ter pelo menos 7 caracteres.', category='error')
            print("SETE")
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            print("Criado")
            return redirect(url_for('views.home'))
    print("GET")

    return render_template("sign_up.html", user=current_user)
