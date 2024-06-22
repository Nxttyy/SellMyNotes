from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from forms import FileUploadForm, RegisterForm, LoginForm
import os, uuid, json
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from extensions import app, db, bcrypt, login_manager
from models import Note, User
from flask_login import login_user, login_required, logout_user, current_user

from handle_payment import handle_chappa

login_manager.login_view = 'login'


with app.app_context():
    db.create_all()


# login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

# @app.before_first_request
# def create_tables():
#     db.create_all()
@app.route('/')
@app.route('/home')
def home():
    
    notes = Note.query.all()

    return render_template('home.html', notes=notes)

@app.route('/upload_product', methods=['GET', 'POST'])
@login_required
def upload_product():

    form = FileUploadForm()

    if form.validate_on_submit():
        _title = form.title.data
        _price = form.price.data
        f = form.note.data

        _, file_extension = os.path.splitext(secure_filename(f.filename))
        filename = uuid.uuid4().hex

        # add note to db
        note = Note(title=_title, filename=filename, price=_price, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()

        f.save(os.path.join(
            app.instance_path, 'uploads', filename+file_extension
        ))

        return redirect(url_for('home'))

    return render_template('upload_product.html', form = form)

@app.route('/handle_payment/<note_id>')
@login_required
def handle_payment(note_id):
    note = Note.query.filter_by(id=note_id).first()
    return_url = url_for('view_note', note_id=note_id)

    conn, payload, headers = handle_chappa(note.price, current_user.email, current_user.first_name, current_user.phone_number, note.title, return_url)

    conn.request("POST", "/v1/transaction/initialize", payload, headers)
    resp = conn.getresponse().read()
    resp = json.loads(resp)
    redirect_url = resp.get("data").get("checkout_url")

    note.poster.earning += note.price
    db.session.commit()

    return redirect(redirect_url)


@app.route('/view_note/<note_id>')
def view_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    src = "./uploads/"+note.filename+".pdf"
    print(src)
    return render_template('note.html',src=src, note=note)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # if form.validate_on_submit() : print(1)
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password= form.password.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

        user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if app.current_user.is_authenticated:  # already logged in
    #     return redirect('/home')
    get_flashed_messages()
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            is_valid = bcrypt.check_password_hash(user.password, password) 
            print(is_valid)

            if is_valid:
                login_user(user, remember=form.remember_me.data)
                return redirect('home')
            else:
                flash("Wrong password")
                return redirect('login')                # wrong password
        else:
            flash("No user with this email.")
            return redirect('login') 
            # wrong email

    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # if session.get('was_once_logged_in'):
    #     # prevent flashing automatically logged out message
    #     del session['was_once_logged_in']
    # flash('You have successfully logged yourself out.')
    return redirect('/login')

@app.route('/account')
def account():

    return render_template('account.html')


if __name__ == '__main__':
    # login_manager.login_view = 'login'
    app.debug = True;
    app.run()