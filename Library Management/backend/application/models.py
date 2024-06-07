from .database import db
from sqlalchemy.orm import relationship

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = relationship('Book', backref='section', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'authors': self.authors,
            'section': self.section.name
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    lastAct = db.Column(db.String)
    user_books = db.relationship('UserBook', backref='user', lazy=True)
    feedbacks = relationship('Feedback', backref='user', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"UserBook('{self.user_id}', '{self.book_id}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Feedback('{self.user_id}', '{self.book_id}')"

class GrantedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    granted_date = db.Column(db.Date, nullable=False)
    granted_user = db.relationship('User', backref='user_granted_books')

    def __repr__(self):
        return f"GrantedBook('{self.user_id}', '{self.book_id}', '{self.granted_date}')"
