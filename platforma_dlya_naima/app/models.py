## app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Candidate(User):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tests = relationship("Test", secondary="candidate_tests", back_populates="candidates")

    __mapper_args__ = {
        'polymorphic_identity':'candidate',
    }

class HR(User):
    __tablename__ = 'hrs'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    candidates = relationship("Candidate", backref="hr")

    __mapper_args__ = {
        'polymorphic_identity':'hr',
    }

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    questions = relationship("Question", back_populates="test")
    candidates = relationship("Candidate", secondary="candidate_tests", back_populates="tests")

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    test = relationship("Test", back_populates="questions")

class CandidateTest(db.Model):
    __tablename__ = 'candidate_tests'
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), primary_key=True)
    test = relationship("Test", backref="candidate_tests")
