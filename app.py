from ast import keyword
from random import choices
from re import S
from turtle import Pen
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/gerejaadb'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
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
    nama = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    wilayah = db.Column(db.Text)
    lingkungan = db.Column(db.Text)
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
    no_kk = db.Column(db.String(50), db.ForeignKey('kartukeluarga.no_kk'))
    # usernya = db.relationship('Profil', backref=db.backref('user', lazy=True))
    userbaptis = db.relationship('Pendaftaranbaptis', backref=db.backref('user', lazy=True))

    def __init__(self, username, password, role, nama, alamat, telepon, wilayah, lingkungan, jeniskelamin, hub, tempat_lahir, tgl_lahir, tempat_baptis, tgl_baptis, tempat_kopertama, gereja_kopertama, tgl_kopertama, tempat_penguatan, gereja_penguatan, tgl_penguatan, tempat_menikah, gereja_menikah, tgl_menikah, pekerjaan, no_kk):
        self.username = username
        if password != '':
            self.password = bcrypt.generate_password_hash(password). decode('UTF-8')
        self.role = role
        self.nama = nama
        self.alamat = alamat
        self.telepon = telepon
        self.wilayah = wilayah
        self.lingkungan = lingkungan
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
        self.no_kk = no_kk

class Kartukeluarga(db.Model):
    __tablename__ = 'kartukeluarga'
    no_kk = db.Column(db.String(50), primary_key=True)
    nama_kk = db.Column(db.String(50))
    kepala_keluarga = db.Column(db.String(50))
    kknya = db.relationship('User', backref=db.backref('kartukeluarga', lazy=True))

    def __init__(self, no_kk, nama_kk, kepala_keluarga):
        self.no_kk = no_kk
        self.nama_kk = nama_kk
        self.kepala_keluarga = kepala_keluarga

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
    no_kk = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterengan = db.Column(db.String(20))

    def __init__(self, nama, nama_baptis, tempat_lahir, tgl_lahir, nama_ayah, nama_ibu, nama_wali, no_kk, alamat, telepon, user_id, keterengan):
        self.nama = nama
        self.nama_baptis = nama_baptis
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.nama_ayah = nama_ayah
        self.nama_ibu = nama_ibu
        self.nama_wali = nama_wali
        self.no_kk = no_kk
        self.alamat = alamat
        self.telepon = telepon
        self.user_id = user_id
        self.keterengan = keterengan

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
                session['username'] = user.username
                session['password'] = user.password
                session['role'] = user.role
                session['nama'] = user.nama
                session['alamat'] = user.alamat
                session['telepon'] = user.telepon
                session['wilayah'] = user.wilayah
                session['lingkungan'] = user.lingkungan
                session['jeniskelamin'] = user.jeniskelamin
                session['hub'] = user.hub
                session['tempat_lahir'] = user.tempat_lahir
                session['tgl_lahir'] = user.tgl_lahir
                session['tempat_baptis'] = user.tempat_baptis
                session['tgl_baptis'] = user.tgl_baptis
                session['tempat_kopertama'] = user.tempat_kopertama
                session['gereja_kopertama'] = user.gereja_kopertama
                session['tgl_kopertama'] = user.tgl_kopertama
                session['tempat_penguatan'] = user.tempat_penguatan
                session['gereja_penguatan'] = user.gereja_penguatan
                session['tgl_penguatan'] = user.tgl_penguatan
                session['tempat_menikah'] = user.tempat_menikah
                session['gereja_menikah'] = user.gereja_menikah
                session['tgl_menikah'] = user.tgl_menikah
                session['pekerjaan'] = user.pekerjaan
                session['no_kk'] = user.no_kk
                return redirect(url_for('dashboard'))
        pesan = "Username atau Password Anda Salah"
        return render_template('login.html', pesan=pesan, forms=forms)
    return render_template('login.html', forms=forms)

# Halaman Dashboard
@app.route('/dashboard')
@login_dulu
def dashboard():
    data = User.query.filter_by(id=id). first()
    return render_template('dashboard.html', data=data)

# Halaman Kelola User
@app.route('/kelola_user')
@login_dulu
def kelola_user():
    data = User.query.filter(User.username != "Admin"). all()
    data1 = Kartukeluarga.query.filter(Kartukeluarga.no_kk != "Admin"). all()
    return render_template('admin/kelola_user.html', data=data, data1=data1)

@app.route('/tambahuser', methods=['GET', 'POST'])
@login_dulu
def tambahuser():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        nama = request.form['nama']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        wilayah = request.form['wilayah']
        lingkungan = request.form['lingkungan']
        jeniskelamin = request.form['jeniskelamin']
        hub = request.form['hub']
        tempat_lahir = request.form['tempat_lahir']
        tgl_lahir = request.form['tgl_lahir']
        tempat_baptis = request.form['tempat_baptis']
        tgl_baptis = request.form['tgl_baptis']
        tempat_kopertama = request.form['tempat_kopertama']
        gereja_kopertama = request.form['gereja_kopertama']
        tgl_kopertama = request.form['tgl_kopertama']
        tempat_penguatan = request.form['tempat_penguatan']
        gereja_penguatan = request.form['gereja_penguatan']
        tgl_penguatan = request.form['tgl_penguatan']
        tempat_menikah = request.form['tempat_menikah']
        gereja_menikah = request.form['gereja_menikah']
        tgl_menikah = request.form['tgl_menikah']
        pekerjaan = request.form['pekerjaan']
        no_kk = request.form['no_kk']
        db.session.add(User(username, password, role, nama, alamat, telepon, wilayah, lingkungan, jeniskelamin, hub, tempat_lahir, tgl_lahir, tempat_baptis, tgl_baptis, tempat_kopertama, gereja_kopertama, tgl_kopertama, tempat_penguatan, gereja_penguatan, tgl_penguatan, tempat_menikah, gereja_menikah, tgl_menikah, pekerjaan, no_kk))
        db.session.commit()
        return redirect(url_for('kelola_user'))

@app.route('/edit_user/<id>', methods=['GET', 'POST'])
@login_dulu
def edit_user(id):
    data = User.query.filter_by(id=id). first()
    if request.method == "POST":
        data.username = request.form['username']
        data.password = request.form['password']
        data.role = request.form['role']
        data.nama = request.form['nama']
        data.alamat = request.form['alamat']
        data.telepon = request.form['telepon']
        data.wilayah = request.form['wilayah']
        data.lingkungan = request.form['lingkungan']
        data.jeniskelamin = request.form['jeniskelamin']
        data.hub = request.form['hub']
        data.tempat_lahir = request.form['tempat_lahir']
        data.tgl_lahir = request.form['tgl_lahir']
        data.tempat_baptis = request.form['tempat_baptis']
        data.tgl_baptis = request.form['tgl_baptis']
        data.tempat_kopertama = request.form['tempat_kopertama']
        data.gereja_kopertama = request.form['gereja_kopertama']
        data.tgl_kopertama = request.form['tgl_kopertama']
        data.tempat_penguatan = request.form['tempat_penguatan']
        data.gereja_penguatan = request.form['gereja_penguatan']
        data.tgl_penguatan = request.form['tgl_penguatan']
        data.tempat_menikah = request.form['tempat_menikah']
        data.gereja_menikah = request.form['gereja_menikah']
        data.tgl_menikah = request.form['tgl_menikah']
        data.pekerjaan = request.form['pekerjaan']
        data.no_kk = request.form['no_kk']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

@app.route('/hapus_user/<id>', methods=['GET', 'POST'])
@login_dulu
def hapus_user(id):
    data = User.query.filter_by(id=id). first()
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)

# Halaman Kelola KK
@app.route('/kelola_kk')
@login_dulu
def kelola_kk():
    data = Kartukeluarga.query.filter(Kartukeluarga.no_kk != "Admin"). all()
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

@app.route('/edit_kk/<no_kk>', methods=['GET', 'POST'])
@login_dulu
def edit_kk(no_kk):
    data = Kartukeluarga.query.filter_by(no_kk=no_kk). first()
    if request.method == "POST":
        data.no_kk = request.form['no_kk']
        data.nama_kk = request.form['nama_kk']
        data.kepala_keluarga = request.form['kepala_keluarga']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman Kelola Umat
@app.route('/kelola_umat')
@login_dulu
def kelola_umat():
    data1 = User.query.all()
    data2 = Kartukeluarga.query.all()
    return render_template('admin/kelola_umat.html', data=data, data1=data1, data2=data2)

# Halaman Umat Baptis Bayi
# @app.route('/baptisbayi')
# @login_dulu

# Halaman Admin Baptis Bayi
@app.route('/admbaptisbayi')
@login_dulu
def admbaptisbayi():
    data = Pendaftaranbaptis.query.filter_by(keterengan="Menunggu Konfirmasi"). all()
    return render_template('admin/baptisbayi.html', data=data)

@app.route('/konfbaptisbayi/<id>', methods=['GET', 'POST'])
@login_dulu
def konfbaptisbayi(id):
    data = Pendaftaranbaptis.query.filter_by(id=id). first()
    if request.method == "POST":
       data.nama = request.form['nama']
       data.nama_baptis = request.form['nama_baptis'] 
       data.tempat_lahir = request.form['tempat_lahir']
       data.tgl_lahir = request.form['tgl_lahir']
       data.nama_ayah = request.form['nama_ayah']
       data.nama_ibu = request.form['nama_ibu']
       data.nama_wali = request.form['nama_wali']
       data.user_id = request.form['user_id']
       data.keterengan = request.form['keterengan']
       db.session.add(data)   
       db.session.commit()
       return redirect(request.referrer)

# Halaman User Baptis Bayi
@app.route('/baptisbayi')
@login_dulu
def baptisbayi():
    data = User.query.filter_by(id=id). first()
    return render_template('user/baptisbayi.html', data=data)

@app.route('/daftarbaptisbayi', methods=['GET', 'POST'])
@login_dulu
def daftarbaptisbayi():
    if request.method == "POST":
        nama = request.form['nama']
        nama_baptis = request.form['nama_baptis']
        tempat_lahir = request.form['tempat_lahir']
        tgl_lahir = request.form['tgl_lahir']
        nama_ayah = request.form['nama_ayah']
        nama_ibu = request.form['nama_ibu']
        nama_wali = request.form['nama_wali']
        no_kk = request.form['no_kk']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        user_id = request.form['user_id']
        keterengan = request.form['keterengan']
        db.session.add(Pendaftaranbaptis(nama, nama_baptis, tempat_lahir, tgl_lahir, nama_ayah, nama_ibu, nama_wali, no_kk, alamat, telepon, user_id, keterengan))
        db.session.commit()
        return redirect(request.referrer)

@app.route('/logout')
@login_dulu
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

