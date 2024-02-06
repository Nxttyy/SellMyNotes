from flask import Flask, render_template, redirect, url_for
from forms import FileUploadForm
import os
from werkzeug.utils import secure_filename


SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload_product', methods=['GET', 'POST'])
def upload_product():

    form = FileUploadForm()

    if form.validate_on_submit():
        f = form.note.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'uploads', filename
        ))
        return redirect(url_for('home'))

    return render_template('upload_product.html', form = form)

if __name__ == '__main__':
    app.debug = True;
    app.run()