from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), unique=False, nullable=False)
    last_name = db.Column(db.String(75), unique=False, nullable=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    earning = db.Column(db.Integer, default=0)
    notes = db.relationship('Note', backref='poster', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.first_name


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    filename = db.Column(db.String(32), unique=True, nullable=False)
    price  = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.title
