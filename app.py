from ast import keyword
from random import choices
from re import S, template
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
    userbaptisbayi = db.relationship('Pendaftaranbaptis', backref=db.backref('user', lazy=True))
    userbaptisdewasa = db.relationship('Baptisdewasa', backref=db.backref('user', lazy=True))
    userperkawinan = db.relationship('Perkawinan', backref=db.backref('user', lazy=True))
    usermisa = db.relationship('Misa', backref=db.backref('user', lazy=True))

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
    __tablename__ = 'daftarbaptisbayi'
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

class Baptisdewasa(db.Model):
    __tablename__ = 'daftarbaptisdewasa'
    id  = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    nama_baptis = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(100))
    tgl_lahir = db.Column(db.String(20))
    agama = db.Column(db.String(20))
    nama_ayah = db.Column(db.String(50))
    nama_ibu = db.Column(db.String(50))
    pasangan = db.Column(db.String(50))
    tgl_menikah = db.Column(db.String(20))
    cara_menikah = db.Column(db.String(50))
    nama_wali = db.Column(db.String(50))
    no_regiskeluarga = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterangan = db.Column(db.String(20))

    def __init__(self, nama, nama_baptis, tempat_lahir, tgl_lahir, agama, nama_ayah, nama_ibu, pasangan, tgl_menikah, cara_menikah, nama_wali, no_regiskeluarga, alamat, telepon, user_id, keterangan):
        self.nama = nama
        self.nama_baptis = nama_baptis
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.agama = agama
        self.nama_ayah = nama_ayah
        self.nama_ibu = nama_ibu
        self.pasangan = pasangan
        self.tgl_menikah = tgl_menikah
        self.cara_menikah = cara_menikah
        self.nama_wali = nama_wali
        self.no_regiskeluarga = no_regiskeluarga
        self.alamat = alamat
        self.telepon = telepon
        self.user_id = user_id
        self.keterangan = keterangan

class Perkawinan(db.Model):
    __tablename__ = "daftarperkawinan"
    id  = db.Column(db.Integer, primary_key=True)
    nama_lk = db.Column(db.String(50))
    tempat_lahir_lk = db.Column(db.String(100))
    tgl_lahir_lk = db.Column(db.String(20))
    agama_lk = db.Column(db.String(20))
    ket_baptis_lk = db.Column(db.String(100))
    no_baptis_lk = db.Column(db.String(50))
    ket_krisma_lk = db.Column(db.String(100))
    no_regiskeluarga_lk = db.Column(db.String(50))
    nama_ayah_lk = db.Column(db.String(50))
    nama_ibu_lk = db.Column(db.String(50))
    pekerjaan_lk = db.Column(db.String(50))
    ket_paroki_lk = db.Column(db.String(100))
    alamat_lk = db.Column(db.Text)
    telepon_lk = db.Column(db.String(15))
    nama_saksi_lk = db.Column(db.String(50))
    dispensasi_lk = db.Column(db.String(50))
    nama_pr = db.Column(db.String(50))
    tempat_lahir_pr = db.Column(db.String(100))
    tgl_lahir_pr = db.Column(db.String(20))
    agama_pr = db.Column(db.String(20))
    ket_baptis_pr = db.Column(db.String(100))
    no_baptis_pr = db.Column(db.String(50))
    ket_krisma_pr = db.Column(db.String(100))
    no_regiskeluarga_pr = db.Column(db.String(50))
    nama_ayah_pr = db.Column(db.String(50))
    nama_ibu_pr = db.Column(db.String(50))
    pekerjaan_pr = db.Column(db.String(50))
    ket_paroki_pr = db.Column(db.String(100))
    alamat_pr = db.Column(db.Text)
    telepon_pr = db.Column(db.String(15))
    nama_saksi_pr = db.Column(db.String(50))
    dispensasi_pr = db.Column(db.String(50))
    alamat_baru = db.Column(db.Text)
    tgl_mohon = db.Column(db.String(20))
    tgl_nikah = db.Column(db.String(20))
    gereja = db.Column(db.String(50))
    alamat_gereja = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterangan = db.Column(db.String(20))

    def __init__(self, nama_lk, tempat_lahir_lk, tgl_lahir_lk, agama_lk, ket_baptis_lk, no_baptis_lk, ket_krisma_lk, no_regiskeluarga_lk, nama_ayah_lk, nama_ibu_lk, pekerjaan_lk, ket_paroki_lk, alamat_lk, telepon_lk, nama_saksi_lk, dispensasi_lk, nama_pr, tempat_lahir_pr, tgl_lahir_pr, agama_pr, ket_baptis_pr, no_baptis_pr, ket_krisma_pr, no_regiskeluarga_pr, nama_ayah_pr, nama_ibu_pr, pekerjaan_pr, ket_paroki_pr, alamat_pr, telepon_pr, nama_saksi_pr, dispensasi_pr, alamat_baru, tgl_mohon, tgl_nikah, gereja, alamat_gereja, user_id, keterangan):
        self.nama_lk = nama_lk
        self.tempat_lahir_lk = tempat_lahir_lk
        self.tgl_lahir_lk = tgl_lahir_lk
        self.agama_lk = agama_lk
        self.ket_baptis_lk = ket_baptis_lk
        self.no_baptis_lk = no_baptis_lk
        self.ket_krisma_lk = ket_krisma_lk
        self.no_regiskeluarga_lk = no_regiskeluarga_lk
        self.nama_ayah_lk = nama_ayah_lk
        self.nama_ibu_lk = nama_ibu_lk
        self.pekerjaan_lk = pekerjaan_lk
        self.ket_paroki_lk = ket_paroki_lk
        self.alamat_lk = alamat_lk
        self.telepon_lk = telepon_lk
        self.nama_saksi_lk = nama_saksi_lk
        self.dispensasi_lk = dispensasi_lk
        self.nama_pr = nama_pr
        self.tempat_lahir_pr = tempat_lahir_pr
        self.tgl_lahir_pr = tgl_lahir_pr
        self.agama_pr = agama_pr
        self.ket_baptis_pr = ket_baptis_pr
        self.no_baptis_pr = no_baptis_pr
        self.ket_krisma_pr = ket_krisma_pr
        self.no_regiskeluarga_pr = no_regiskeluarga_pr
        self.nama_ayah_pr = nama_ayah_pr
        self.nama_ibu_pr = nama_ibu_pr
        self.pekerjaan_pr = pekerjaan_pr
        self.ket_paroki_pr = ket_paroki_pr
        self.alamat_pr = alamat_pr
        self.telepon_pr = telepon_pr
        self.nama_saksi_pr = nama_saksi_pr
        self.dispensasi_pr = dispensasi_pr
        self.alamat_baru = alamat_baru
        self.tgl_mohon = tgl_mohon
        self.tgl_nikah = tgl_nikah
        self.gereja = gereja
        self.alamat_gereja = alamat_gereja
        self.user_id = user_id
        self.keterangan = keterangan

class Misa(db.Model):
    __tablename__ = "daftarmisa"
    id = db.Column(db.Integer, primary_key=True)
    intensi = db.Column(db.String(50))
    hari_tgl = db.Column(db.String(30))
    jam = db.Column(db.String(10))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    lingkungan = db.Column(db.Text)
    wilayah = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterangan = db.Column(db.String(20))

    def __init__(self, intensi, hari_tgl, jam, alamat, telepon, lingkungan, wilayah, user_id, keterangan):
        self.intensi = intensi
        self.hari_tgl = hari_tgl
        self.jam = jam
        self.alamat = alamat
        self.telepon = telepon
        self.lingkungan = lingkungan
        self.wilayah = wilayah
        self.user_id = user_id
        self.keterangan = keterangan

class Komunipertama(db.Model):
    __tablename__ = "daftarkomunipertama"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    nama_pemandian = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(20))
    tgl_lahir = db.Column(db.String(20))
    tempat_pemandian = db.Column(db.String(50))
    tgl_pemandian = db.Column(db.String(20))
    nama_ayah = db.Column(db.String(50))
    nama_ibu = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    wilayah = db.Column(db.Text)
    lingkungan = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    sekolah = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterangan = db.Column(db.String(20))

    def __init__(self, nama, nama_pemandian, tempat_lahir, tgl_lahir, tempat_pemandian, tgl_pemandian, nama_ayah, nama_ibu, alamat, wilayah, lingkungan, telepon, sekolah, user_id, keterangan):
        self.nama = nama
        self.nama_pemandian = nama_pemandian
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.tempat_pemandian = tempat_pemandian
        self.tgl_pemandian = tgl_pemandian
        self.nama_ayah = nama_ayah
        self.nama_ibu = nama_ibu
        self.alamat = alamat
        self.wilayah = wilayah
        self.lingkungan = lingkungan
        self.telepon = telepon
        self.sekolah = sekolah
        self.user_id = user_id
        self.keterangan = keterangan

class Pengantarlingkungan(db.Model):
    __tablename__ = 'daftarpengantarlingkungan'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    status_pekerjaan = db.Column(db.String(10))
    tempat_lahir = db.Column(db.String(20))
    tgl_lahir = db.Column(db.String(20))
    no_kk = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(15))
    lingkungan = db.Column(db.Text)
    wilayah = db.Column(db.Text)
    keperluan = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keterangan = db.Column(db.String(20))

    def __init__(self, nama, status_pekerjaan, tempat_lahir, tgl_lahir, no_kk, alamat, telepon, lingkungan, wilayah, keperluan, user_id, keterangan):
        self.nama = nama
        self.status_pekerjaan = status_pekerjaan
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.no_kk = no_kk
        self.alamat = alamat
        self.telepon = telepon
        self.lingkungan = lingkungan
        self.wilayah = wilayah
        self.keperluan = keperluan
        self.user_id = user_id
        self.keterangan = keterangan

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
    data1 = Baptisdewasa.query.filter_by(id=id). all()
    return render_template('dashboard.html', data=data, data1=data1)

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

# Halaman Admin Baptis Dewasa
@app.route('/admbaptisdewasa')
@login_dulu
def admbaptisdewasa():
    data = Baptisdewasa.query.filter_by(keterangan="Menunggu Konfirmasi"). all()
    return render_template('admin/baptisdewasa.html', data=data)

@app.route('/konfbaptisdewasa/<id>', methods=['GET', 'POST'])
@login_dulu
def konfbaptisdewasa(id):
    data = Baptisdewasa.query.filter_by(id=id). first()
    if request.method == "POST":
        data.nama = request.form['nama']
        data.nama_baptis = request.form['nama_baptis']
        data.tempat_lahir = request.form['tempat_lahir']
        data.tgl_lahir = request.form['tgl_lahir']
        data.agama = request.form['agama']
        data.nama_ayah = request.form['nama_ayah']
        data.nama_ibu = request.form['nama_ibu']
        data.pasangan = request.form['pasangan']
        data.tgl_menikah = request.form['tgl_menikah']
        data.cara_menikah = request.form['cara_menikah']
        data.nama_wali = request.form['nama_wali']
        data.no_regiskeluarga = request.form['no_regiskeluarga']
        data.alamat = request.form['alamat']
        data.telepon = request.form['telepon']
        data.user_id = request.form['user_id']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman User Baptis Dewasa
@app.route('/baptisdewasa')
@login_dulu
def baptisdewasa():
    data = User.query.filter_by(id=id). first()
    return render_template('user/baptisdewasa.html', data=data)

@app.route('/daftarbaptisdewasa', methods=['GET', 'POST'])
@login_dulu
def daftarbaptisdewasa():
    if request.method == "POST":
        nama = request.form['nama']
        nama_baptis = request.form['nama_baptis']
        tempat_lahir = request.form['tempat_lahir']
        tgl_lahir = request.form['tgl_lahir']
        agama = request.form['agama']
        nama_ayah = request.form['nama_ayah']
        nama_ibu = request.form['nama_ibu']
        pasangan = request.form['pasangan']
        tgl_menikah = request.form['tgl_menikah']
        cara_menikah = request.form['cara_menikah']
        nama_wali = request.form['nama_wali']
        no_regiskeluarga = request.form['no_regiskeluarga']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        user_id = request.form['user_id']
        keterangan = request.form['keterangan']
        db.session.add(Baptisdewasa(nama, nama_baptis, tempat_lahir, tgl_lahir, agama, nama_ayah, nama_ibu, pasangan, tgl_menikah, cara_menikah, nama_wali, no_regiskeluarga, alamat, telepon, user_id, keterangan))
        db.session.commit()
        return redirect(request.referrer)

# Halaman Admin Perkawinan
@app.route('/admperkawinan')
@login_dulu
def admperkawinan():
    data = Perkawinan.query.filter_by(keterangan="Menunggu Konfirmasi"). all()
    return render_template('admin/perkawinan.html', data=data)

@app.route('/konfperkawinan/<id>', methods=['GET', 'POST'])
@login_dulu
def konfperkawinan(id):
    data = Perkawinan.query.filter_by(id=id). first()
    if request.method == "POST":
        data.nama_lk = request.form['nama_lk']
        data.tempat_lahir_lk = request.form['tempat_lahir_lk']
        data.tgl_lahir_lk = request.form['tgl_lahir_lk']
        data.agama_lk = request.form['agama_lk']
        data.ket_baptis_lk = request.form['ket_baptis_lk']
        data.no_baptis_lk = request.form['no_baptis_lk']
        data.ket_krisma_lk = request.form['ket_krisma_lk']
        data.no_regiskeluarga_lk = request.form['no_regiskeluarga_lk']
        data.nama_ayah_lk = request.form['nama_ayah_lk']
        data.nama_ibu_lk = request.form['nama_ibu_lk']
        data.pekerjaan_lk = request.form['pekerjaan_lk']
        data.ket_paroki_lk = request.form['ket_paroki_lk']
        data.alamat_lk = request.form['alamat_lk']
        data.telepon_lk = request.form['telepon_lk']
        data.nama_saksi_lk = request.form['nama_saksi_lk']
        data.dispensasi_lk = request.form['dispensasi_lk']
        data.nama_pr = request.form['nama_pr']
        data.tempat_lahir_pr = request.form['tempat_lahir_pr']
        data.tgl_lahir_pr = request.form['tgl_lahir_pr']
        data.agama_pr = request.form['agama_pr']
        data.ket_baptis_pr = request.form['ket_baptis_pr']
        data.no_baptis_pr = request.form['no_baptis_pr']
        data.ket_krisma_pr = request.form['ket_krisma_pr']
        data.no_regiskeluarga_pr = request.form['no_regiskeluarga_pr']
        data.nama_ayah_pr = request.form['nama_ayah_pr']
        data.nama_ibu_pr = request.form['nama_ibu_pr']
        data.pekerjaan_pr = request.form['pekerjaan_pr']
        data.ket_paroki_pr = request.form['ket_paroki_pr']
        data.alamat_pr = request.form['alamat_pr']
        data.telepon_pr = request.form['telepon_pr']
        data.nama_saksi_pr = request.form['nama_saksi_pr']
        data.dispensasi_pr = request.form['dispensasi_pr']
        data.alamat_baru = request.form['alamat_baru']
        data.tgl_mohon = request.form['tgl_mohon']
        data.tgl_nikah = request.form['tgl_nikah']
        data.gereja = request.form['gereja']
        data.alamat_gereja = request.form['alamat_gereja']
        data.user_id = request.form['user_id']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman User Perkawinan
@app.route('/perkawinan')
@login_dulu
def perkawinan():
    return render_template('user/perkawinan.html')

@app.route('/daftarperkawinan', methods=['GET', 'POST'])
@login_dulu
def daftarperkawinan():
    if request.method == "POST":
        nama_lk = request.form['nama_lk']
        tempat_lahir_lk = request.form['tempat_lahir_lk']
        tgl_lahir_lk = request.form['tgl_lahir_lk']
        agama_lk = request.form['agama_lk']
        ket_baptis_lk = request.form['ket_baptis_lk']
        no_baptis_lk = request.form['no_baptis_lk']
        ket_krisma_lk = request.form['ket_krisma_lk']
        no_regiskeluarga_lk = request.form['no_regiskeluarga_lk']
        nama_ayah_lk = request.form['nama_ayah_lk']
        nama_ibu_lk = request.form['nama_ibu_lk']
        pekerjaan_lk = request.form['pekerjaan_lk']
        ket_paroki_lk = request.form['ket_paroki_lk']
        alamat_lk = request.form['alamat_lk']
        telepon_lk = request.form['telepon_lk']
        nama_saksi_lk = request.form['nama_saksi_lk']
        dispensasi_lk = request.form['dispensasi_lk']
        nama_pr = request.form['nama_pr']
        tempat_lahir_pr = request.form['tempat_lahir_pr']
        tgl_lahir_pr = request.form['tgl_lahir_pr']
        agama_pr = request.form['agama_pr']
        ket_baptis_pr = request.form['ket_baptis_pr']
        no_baptis_pr = request.form['no_baptis_pr']
        ket_krisma_pr = request.form['ket_krisma_pr']
        no_regiskeluarga_pr = request.form['no_regiskeluarga_pr']
        nama_ayah_pr = request.form['nama_ayah_pr']
        nama_ibu_pr = request.form['nama_ibu_pr']
        pekerjaan_pr = request.form['pekerjaan_pr']
        ket_paroki_pr = request.form['ket_paroki_pr']
        alamat_pr = request.form['alamat_pr']
        telepon_pr = request.form['telepon_pr']
        nama_saksi_pr = request.form['nama_saksi_pr']
        dispensasi_pr = request.form['dispensasi_pr']
        alamat_baru = request.form['alamat_baru']
        tgl_mohon = request.form['tgl_mohon']
        tgl_nikah = request.form['tgl_nikah']
        gereja = request.form['gereja']
        alamat_gereja = request.form['alamat_gereja']
        user_id = request.form['user_id']
        keterangan = request.form['keterangan']
        db.session.add(Perkawinan(nama_lk, tempat_lahir_lk, tgl_lahir_lk, agama_lk, ket_baptis_lk, no_baptis_lk, ket_krisma_lk, no_regiskeluarga_lk, nama_ayah_lk, nama_ibu_lk, pekerjaan_lk, ket_paroki_lk, alamat_lk, telepon_lk, nama_saksi_lk, dispensasi_lk, nama_pr, tempat_lahir_pr, tgl_lahir_pr, agama_pr, ket_baptis_pr, no_baptis_pr, ket_krisma_pr, no_regiskeluarga_pr, nama_ayah_pr, nama_ibu_pr, pekerjaan_pr, ket_paroki_pr, alamat_pr, telepon_pr, nama_saksi_pr, dispensasi_pr, alamat_baru, tgl_mohon, tgl_nikah, gereja, alamat_gereja, user_id, keterangan))
        db.session.commit()
        return redirect(request.referrer)

# Halaman Admin Misa
@app.route('/admmisa')
@login_dulu
def admmisa():
    data = Misa.query.filter_by(keterangan="Menunggu Konfirmasi"). all()
    return render_template('admin/misa.html', data=data)

@app.route('/konfmisa/<id>', methods=['GET', 'POST'])
@login_dulu
def konfmisa(id):
    data = Misa.query.filter_by(id=id). first()
    if request.method == "POST":
        data.intensi = request.form['intensi']
        data.hari_tgl = request.form['hari_tgl']
        data.jam = request.form['jam']
        data.alamat = request.form['alamat']
        data.telepon = request.form['telepon']
        data.lingkungan = request.form['lingkungan']
        data.wilayah = request.form['wilayah']
        data.user_id = request.form['user_id']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman User Misa
@app.route('/misa')
@login_dulu
def misa():
    data = User.query.filter_by(id=id). first()
    return render_template('user/misa.html', data=data)

@app.route('/daftarmisa', methods=['GET', 'POST'])
@login_dulu
def daftarmisa():
    if request.method == "POST":
        intensi = request.form['intensi']
        hari_tgl = request.form['hari_tgl']
        jam = request.form['jam']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        lingkungan = request.form['lingkungan']
        wilayah = request.form['wilayah']
        user_id = request.form['user_id']
        keterangan = request.form['keterangan']
        db.session.add(Misa(intensi, hari_tgl, jam, alamat, telepon, lingkungan, wilayah, user_id, keterangan))
        db.session.commit()
        return redirect(request.referrer)

# Halaman Admin Komuni Pertama
@app.route('/admkomunipertama')
@login_dulu
def admkomunipertama():
    data = Komunipertama.query.filter_by(keterangan="Menunggu Konfirmasi"). all()
    return render_template('admin/komunipertama.html', data=data)

@app.route('/konfkomunipertama/<id>', methods=['GET', 'POST'])
@login_dulu
def konfkomunipertama(id):
    data = Komunipertama.query.filter_by(id=id). first()
    if request.method == "POST":
        data.nama = request.form['nama']
        data.nama_pemandian = request.form['nama_pemandian']
        data.tempat_lahir = request.form['tempat_lahir']
        data.tgl_lahir = request.form['tgl_lahir']
        data.tempat_pemandian = request.form['tempat_pemandian']
        data.tgl_pemandian = request.form['tgl_pemandian']
        data.nama_ayah = request.form['nama_ayah']
        data.nama_ibu = request.form['nama_ibu']
        data.alamat = request.form['alamat']
        data.wilayah = request.form['wilayah']
        data.lingkungan = request.form['lingkungan']
        data.telepon = request.form['telepon']
        data.sekolah = request.form['sekolah']
        data.user_id = request.form['user_id']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman User Komuni Pertama
@app.route('/komunipertama')
@login_dulu
def komunipertama():
    data = Komunipertama.query.filter_by(id=id). first()
    return render_template('user/komunipertama.html', data=data)

@app.route('/daftarkomunipertama', methods=['GET', 'POST'])
@login_dulu
def daftarkomunipertama():
    if request.method == "POST":
        nama = request.form['nama']
        nama_pemandian = request.form['nama_pemandian']
        tempat_lahir = request.form['tempat_lahir']
        tgl_lahir = request.form['tgl_lahir']
        tempat_pemandian = request.form['tempat_pemandian']
        tgl_pemandian = request.form['tgl_pemandian']
        nama_ayah = request.form['nama_ayah']
        nama_ibu = request.form['nama_ibu']
        alamat = request.form['alamat']
        wilayah = request.form['wilayah']
        lingkungan = request.form['lingkungan']
        telepon = request.form['telepon']
        sekolah = request.form['sekolah']
        user_id = request.form['user_id']
        keterangan = request.form['keterangan']
        db.session.add(Komunipertama(nama, nama_pemandian, tempat_lahir, tgl_lahir, tempat_pemandian, tgl_pemandian, nama_ayah, nama_ibu, alamat, wilayah, lingkungan, telepon, sekolah, user_id, keterangan))
        db.session.commit()
        return redirect(request.referrer)

# Halaman Admin Pengantar Lingkungan
@app.route('/admpengantarlingkungan')
@login_dulu
def admpengantarlingkungan():
    data = Pengantarlingkungan.query.filter_by(keterangan="Menunggu Konfirmasi"). all()
    return render_template('admin/pengantarlingkungan.html', data=data)

@app.route('/konfpengantarlingkungan/<id>', methods=['GET', 'POST'])
@login_dulu
def konfpengantarlingkungan(id):
    data = Pengantarlingkungan.query.filter_by(id=id). first()
    if request.method == "POST":
        data.nama = request.form['nama']
        data.status_pekerjaan = request.form['status_pekerjaan']
        data.tempat_lahir = request.form['tempat_lahir']
        data.tgl_lahir = request.form['tgl_lahir']
        data.no_kk = request.form['no_kk']
        data.alamat = request.form['alamat']
        data.telepon = request.form['telepon']
        data.lingkungan = request.form['lingkungan']
        data.wilayah = request.form['wilayah']
        data.keperluan = request.form['keperluan']
        data.user_id = request.form['user_id']
        data.keterangan = request.form['keterangan']
        db.session.add(data)
        db.session.commit()
        return redirect(request.referrer)

# Halaman User Pengantar Lingkungan
@app.route('/pengantarlingkungan')
@login_dulu
def pengantarlingkungan():
    data = User.query.filter_by(id=id). first()
    return render_template('user/pengantarlingkungan.html')

@app.route('/daftarpengantarlingkungan', methods=['GET', 'POST'])
@login_dulu
def daftarpengantarlingkungan():
    if request.method == "POST":
        nama = request.form['nama']
        status_pekerjaan = request.form['status_pekerjaan']
        tempat_lahir = request.form['tempat_lahir']
        tgl_lahir = request.form['tgl_lahir']
        no_kk = request.form['no_kk']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        lingkungan = request.form['lingkungan']
        wilayah = request.form['wilayah']
        keperluan = request.form['keperluan']
        user_id = request.form['user_id']
        keterangan = request.form['keterangan']
        db.session.add(Pengantarlingkungan(nama, status_pekerjaan, tempat_lahir, tgl_lahir, no_kk, alamat, telepon, lingkungan, wilayah, keperluan, user_id, keterangan))
        db.session.commit()
        return redirect(request.referrer)


@app.route('/logout')
@login_dulu
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

