from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash
from . import db, app
from .models import User, Candidate, HR, Test
from .forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard')
            return redirect(next_page)
        else:
            flash('Invalid email or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering user: {e}')
            return redirect(url_for('register'))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if isinstance(current_user, Candidate):
        tests = current_user.tests
        return render_template('dashboard.html', title='Dashboard', tests=tests)
    elif isinstance(current_user, HR):
        candidates = current_user.candidates
        return render_template('dashboard.html', title='Dashboard', candidates=candidates)
    else:
        return redirect(url_for('index'))

@app.route('/test/<test_id>')
@login_required
def test(test_id):
    test = Test.query.get(test_id)
    if test is None:
        flash('Test not found.')
        return redirect(url_for('dashboard'))
    if isinstance(current_user, Candidate) and test not in current_user.tests:
        flash('Access unauthorized.')
        return redirect(url_for('dashboard'))
    if isinstance(current_user, HR) and not any(test in candidate.tests for candidate in current_user.candidates):
        flash('Access unauthorized.')
        return redirect(url_for('dashboard'))
    return render_template('test.html', title=test.title, test=test)
