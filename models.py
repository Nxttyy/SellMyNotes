from extensions import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    filename = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.title