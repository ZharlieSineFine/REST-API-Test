from flask import Flask, request

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.name, 'description': book.description}
        output.append(book_data)

    return {"books": output}


@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return {"name": book.name, "description": book.description}


@app.route('/books/<int:book_id>', methods=['POST'])
def add_book(book_id):
    book = Book(name=request.json['name'], description=request.json['description'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}
