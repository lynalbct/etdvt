from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from app import db, app
from app.forms import *
from app.models import *
from flask import render_template, request, url_for,redirect,send_from_directory
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import flash

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Researcher.query.get(user_id)

@app.route('/')
def index():
	return render_template('landing/index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        user = Researcher.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
                return render_template('forms/login.html', form=form)
        else:
            return render_template('forms/login.html', form=form)

    return render_template('forms/login.html', form=form)

# @app.route('/register', methods = ['GET','POST'])
# def register():
# 	form = RegistrationForm()

# 	if current_user.is_authenticated is True:
# 		return redirect(url_for('home'))
# 	if request.method == 'POST':
# 		if form.validate_on_submit():
# 			new_user = Researcher(form.username.data, form.password.data, form.first_name.data,\
# 					form.last_name.data, form.email.data, form.profession.data, form.organization.data)
# 			print('hello')
# 			db.session.add(new_user)
# 			db.session.commit()
# 			if new_user is True:
# 				print('hello')	
# 				login_user(new_user, remember=True)
# 				return redirect(url_for('index'))
# 			return redirect(url_for('home'))
# 	return render_template('forms/registration.html', form=form)
@app.route('/reg')
def reg():
	form = RegistrationForm()
	return render_template('forms/registration.html', form=form)

@app.route('/register', methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('YEY')
		new = Researcher(form.username.data, form.password.data, form.first_name.data,\
					form.last_name.data, form.email.data, form.profession.data, form.organization.data)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('home'))
	return jsonify('data')


@app.route('/home')
def home():
	return render_template('dashboard/dashboard.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))