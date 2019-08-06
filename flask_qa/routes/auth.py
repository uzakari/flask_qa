from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_qa.extentions import db
from flask_login import login_user
from werkzeug.security import check_password_hash


from flask_qa.models import User, Question

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        unhashed_password = request.form['password']

        user = User(
            name=name,
            unhashed_password=unhashed_password,
            expert=False,
            admin=False
        )
        user_exist=User.query.filter_by(name=name).first()
        if user_exist and check_password_hash(user_exist.password, unhashed_password):
            flash('User with those credential exist already')
            return redirect(url_for('auth.register'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid User')
        else:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')
 