from vault import app
from flask import render_template, redirect, url_for, flash ,session,request
from vault.models import User
from vault.forms import RegisterForm, LoginForm
from vault import db
from vault.users import create_table,insert
from vault.retrieve import show
from flask_login import login_user, logout_user, login_required
from vault.encdec import decrypt,encrypt


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    db.create_all()
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f"Account created successfully! You can log in with username", category='success')
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'username' not in session:
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                session['username'] = attempted_user.username
                return redirect(url_for('vault_page'))
            else:
                flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    session.pop('username', None)
    return redirect(url_for("login_page"))


@app.route('/vault',methods=['GET'])
@login_required
def vault_page():
    if 'username' in session:
        return render_template('vault.html')

@app.route('/password',methods=['POST','GET'])
def passwords_page():
        return render_template('pass.html')
    
@app.route('/passwords',methods=['POST','GET'])
def show_passwords():
    if 'username' in session:
        # Fetch data corresponding to the logged-in user
        passw=request.form.get('passw')
        user_data=show(username=session['username'],passw=passw)
        return render_template('passwords.html',user_data=user_data)



@app.route('/store',methods=['POST'])
def store_page():
    name,email,website,password,password1 = request.form.get('name'),request.form.get('email_address'),request.form.get('website_name'),request.form.get('password'),request.form.get('password1')
    user_to_create = create_table(username=session['username'])
    password_st=encrypt(data=password,password=password1)
    insert(user1=session['username'],username=name,
                              email=email,
                              password=password_st,
                              website=website)
    flash(f"data created successfully! ", category='success')
    return render_template('store.html')