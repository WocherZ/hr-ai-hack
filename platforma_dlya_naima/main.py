from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Candidate, HR, Test, Question, db
from app.forms import LoginForm, RegistrationForm, TestSubmissionForm

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/')
# #@login_required
# def dashboard():
#     # if isinstance(current_user, Candidate):
#     #     tests = Test.query.all()
#     #     return render_template('dashboard.html', tests=tests, user_type='candidate')
#     # elif isinstance(current_user, HR):
#     #     candidates = Candidate.query.all()
#     #     return render_template('dashboard.html', candidates=candidates, user_type='hr')
#     # return redirect(url_for('login'))
#
#     return render_template('home.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/candidate')
def candidate_page():
    return render_template('candidate.html')

@app.route('/hr')
def hr_page():
    pass
    return render_template('hr.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #db.create_all()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test(test_id):
    test = Test.query.get_or_404(test_id)
    form = TestSubmissionForm()
    if form.validate_on_submit():
        # Here, you would implement the logic to process the submitted answers.
        # This could involve comparing the submitted answers with the correct ones,
        # calculating a score, and then updating the database with the candidate's performance.
        # For demonstration purposes, we'll just show a flash message.
        flash('Test submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('test.html', test=test, form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
