from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from app.models import User, Candidate, HR, Test, Question, db
# from app.forms import LoginForm, RegistrationForm, TestSubmissionForm

app = Flask(__name__, template_folder='app/templates/', static_folder='app/static/')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/candidate')
def candidate_page():
    return render_template('candidate.html')


@app.route('/hr')
def hr_page():
    return render_template('hr.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/create_test/<int:test_id>')
def create_test_page(test_id):

    return render_template('create_test.html')


if __name__ == '__main__':
    app.run(debug=True)
