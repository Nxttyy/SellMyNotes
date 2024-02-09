from flask import Flask, render_template, redirect, url_for
from forms import FileUploadForm
import os, uuid
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from extensions import app, db
from models import Note

@app.route('/')
def home():
    
    notes = Note.query.all()

    return render_template('home.html', notes=notes)

@app.route('/upload_product', methods=['GET', 'POST'])
def upload_product():

    form = FileUploadForm()

    if form.validate_on_submit():
        _title = form.title.data
        f = form.note.data

        _, file_extension = os.path.splitext(secure_filename(f.filename))
        filename = uuid.uuid4().hex

        # add note to db
        note = Note(title=_title, filename=filename)
        db.session.add(note)
        db.session.commit()

        f.save(os.path.join(
            app.instance_path, 'uploads', filename+file_extension
        ))

        return redirect(url_for('home'))

    return render_template('upload_product.html', form = form)

if __name__ == '__main__':
    app.debug = True;
    app.run()