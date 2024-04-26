from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.file_manager import JsonFileManager
from app.new_file_manager import NewJsonFileManager
import os


app = Flask(__name__, template_folder='app/templates/', static_folder='app/static/')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
file_path = os.path.join(os.path.dirname(__file__), 'app', 'tests_new.json')
new_file_manager = NewJsonFileManager(file_path)


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


# Создание тестов HR
@app.route('/create_test/<int:test_id>')
def create_test_page(test_id):
    test_db = JsonFileManager('app/tests.json')
    test_data = test_db.get_data_by_key(test_id)

    return render_template('create_test.html', test_data=test_data)

@app.route('/hr/test/')
def create_hr_test_page():
    theme = request.args.get('theme')
    question_count = request.args.get('questionCount')
    # file_path = os.path.join(os.path.dirname(__file__), 'app', 'tests_new.json')
    test_data = new_file_manager.get_data_by_theme(theme)

    return render_template('create_test.html', theme=theme, test_data=test_data)

@app.route('/hr/test/save', methods=['POST'])
def save_test():
    if request.method == 'POST':
        data = request.get_json()  # Получаем данные из запроса в формате JSON
        theme = data.get('theme')  # Извлекаем значение theme
        questions = data.get('questions')
        # test_questions = request.json  # Получаем список вопросов и ответов из запроса
        new_file_manager.add_questions(theme, questions)
        new_file_manager.save_json()
        # Здесь можно выполнить логику для сохранения теста, например, в базу данных
        # Пример сохранения теста в виде JSON файла
        return render_template('create_test.html', theme=theme, test_data=questions)

@app.route('/test/<int:test_id>')
def test_page(test_id):
    test_db = JsonFileManager('app/tests.json')
    test_data = test_db.get_data_by_key(test_id)

    return render_template('test.html', test_data=test_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
