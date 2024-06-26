# ## app/forms.py
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
# from app.models import User
#
# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Введите ваш email"})
#     password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Введите ваш пароль"})
#     # email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите ваш email"})
#     # password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Введите ваш пароль"})
#     submit = SubmitField('Войти')
#
# class RegistrationForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Введите ваш email"})
#     password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
#     # email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите ваш email"})
#     # password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Подтвердите ваш пароль"})
#     submit = SubmitField('Регистрация')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Этот email уже используется. Пожалуйста, используйте другой email.')
#
#
# class TestSubmissionForm(FlaskForm):
#     answer_1 = StringField('Answer 1', validators=[DataRequired()], render_kw={"placeholder": "Enter your answer for question 1"})
#     answer_2 = StringField('Answer 2', validators=[DataRequired()], render_kw={"placeholder": "Enter your answer for question 2"})
#     # Add more answer fields as needed for the test questions
#     submit = SubmitField('Submit')
