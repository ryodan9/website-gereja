from ast import keyword
from random import choices
from re import S
from wsgiref.validate import validator
from flask import Flask, jsonify, render_template, request, redirect, request, url_for, session, flash, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from functools import wraps
from flask_migrate import Migrate
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '$#PHenfge24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/dbgereja'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

class Login(FlaskForm):
    username = StringField('', validators=[InputRequired()],
    render_kw={'autofocus':True, 'placeholder':'Username'})
    password = PasswordField('', validators=[InputRequired()],
    render_kw={'autofocus':True, 'placeholder':'Password'})
    role = SelectField('', validators=[InputRequired()], choices=[('Admin','Admin'), ('Umat', 'Umat')])

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)
    role = db.Column(db.String(10))
    usernya = db.relationship('Profil', backref=db.backref('user'), lazy=True)
    userbaptis = db.relationship('Pendaftaranbaptis', backref=db.backref('user'), lazy=True)

    def __init__(self, username, password, role):
        self.username = username
        if password != '':
            self.password = bcrypt.generate_password_hash(password). decode('UTF-8')
        self.role = role

class Kartukeluarga(db.Model):
    __tablename__ = 'kartukeluarga'
    id = db.Column(db.Integer, primary_key=True)
    no_kk = db.Column(db.String(50))
    nama_kk = db.Column(db.String(50))
    kepala_keluarga = db.Column(db.String(50))
    kkprofil = db.relationship('Profil', backref=db.backref('kartukeluarga'), lazy=True)

    def __init__(self, no_kk, nama_kk, kepala_keluarga):
        self.no_kk = no_kk
        self.nama_kk = nama_kk
        self.kepala_keluarga = kepala_keluarga

class Profil(db.Model):
    __tablename__ = 'profil'
    id = db.Column(db.Integer, primary_key=True)
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    wilayah = db.Column(db.Text)
    lingkungan = db.Column(db.Text)
    nama = db.Column(db.String(50))
    jeniskelamin = db.Column(db.String(10))
    hub = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(100))
    tgl_lahir = db.Column(db.String(20))
    tempat_baptis = db.Column(db.Text)
    tgl_baptis = db.Column(db.String(20))
    tempat_kopertama = db.Column(db.Text)
    gereja_kopertama = db.Column(db.String(50))
    tgl_kopertama = db.Column(db.String(20))
    tempat_penguatan = db.Column(db.String(50))
    gereja_penguatan = db.Column(db.String(50))
    tgl_penguatan = db.Column(db.String(20))
    tempat_menikah = db.Column(db.String(50))
    gereja_menikah = db.Column(db.String(50))
    tgl_menikah = db.Column(db.String(20))
    pekerjaan = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    kartukeluarga_id = db.Column(db.Integer, db.ForeignKey('kartukeluarga.id'))

    def __init__(self, alamat, telepon, wilayah, lingkungan, nama, jeniskelamin, hub, tempat_lahir, tgl_lahir, tempat_baptis, tgl_baptis, tempat_kopertama, gereja_kopertama, tgl_kopertama, tempat_penguatan, gereja_penguatan, tgl_penguatan, tempat_menikah, gereja_menikah, tgl_menikah, pekerjaan, user_id):
        self.alamat = alamat
        self.telepon = telepon
        self.wilayah = wilayah
        self.lingkungan = lingkungan
        self.nama = nama
        self.jeniskelamin = jeniskelamin
        self.hub = hub
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.tempat_baptis = tempat_baptis
        self.tgl_baptis = tgl_baptis
        self.tempat_kopertama = tempat_kopertama
        self.gereja_kopertama = gereja_kopertama
        self.tgl_kopertama = tgl_kopertama
        self.tempat_penguatan = tempat_penguatan
        self.gereja_penguatan = gereja_penguatan
        self.tgl_penguatan = tgl_penguatan
        self.tempat_menikah = tempat_menikah
        self.gereja_menikah = gereja_menikah
        self.tgl_menikah = tgl_menikah
        self.pekerjaan = pekerjaan
        self.user_id = user_id

class Pendaftaranbaptis(db.Model):
    __tablename__ = 'daftarbaptis'
    id  = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    nama_baptis = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(100))
    tgl_lahir = db.Column(db.String(20))
    nama_ayah = db.Column(db.String(50))
    nama_ibu = db.Column(db.String(50))
    nama_wali = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, nama, nama_baptis, tempat_lahir, tgl_lahir, nama_ayah, nama_ibu, nama_wali, user_id):
        self.nama = nama
        self.nama_baptis = nama_baptis
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.nama_ayah = nama_ayah
        self.nama_ibu = nama_ibu
        self.nama_wali = nama_wali
        self.user_id = user_id

db.create_all()

def login_dulu(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    if session.get('login') == True:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Halaman Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('login') == True:
        return redirect(url_for('dashboard'))
    forms = Login()
    if forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data). first()
        if user:
            if bcrypt.check_password_hash(user.password, forms.password.data):
                session['login'] = True
                session['id'] = user.id
                session['role'] = user.role
                return redirect(url_for('dashboard'))
        pesan = "Username atau Password Anda Salah"
        return render_template('login.html', pesan=pesan, forms=forms)
    return render_template('login.html', forms=forms)

# Halaman Dashboard
@app.route('/dashboard')
@login_dulu
def dashboard():
    return render_template('dashboard.html')

# Halaman Kelola User
@app.route('/kelola_user')
@login_dulu
def kelola_user():
    data = User.query.all()
    return render_template('admin/kelola_user.html', data=data)

@app.route('/tambahuser', methods=['GET', 'POST'])
@login_dulu
def tambahuser():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db.session.add(User(username, password, role))
        db.session.commit()
        return redirect(url_for('kelola_user'))

# Halaman Kelola KK
@app.route('/kelola_kk')
@login_dulu
def kelola_kk():
    data = Kartukeluarga.query.all()
    return render_template('admin/kelola_kk.html', data=data)

@app.route('/tambah_kk', methods=['GET', 'POST'])
@login_dulu
def tambah_kk():
    if request.method == "POST":
        no_kk = request.form['no_kk']
        nama_kk = request.form['nama_kk']
        kepala_keluarga = request.form['kepala_keluarga']
        db.session.add(Kartukeluarga(no_kk, nama_kk, kepala_keluarga))
        db.session.commit()
        return redirect(request.referrer)
# Halaman Umat Baptis Bayi
# @app.route('/baptisbayi')

# Halaman Admin Baptis Bayi
@app.route('/admbaptisbayi')
def admbaptisbayi():
    # data = Baptisbayi.query.filter_by(keterangan="Menunggu Konfirmasi")
    return render_template('admin/baptisbayi.html')


# @app.route('/konfbaptisbayi/<id>', methods=['GET', 'POST'])


@app.route('/logout')
@login_dulu
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

