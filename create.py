from app import db, User, Kartukeluarga

# jumlah_kursi = "100"
# db.session.add(Status(jumlah_kursi))
# db.session.commit()

# jumlah_kursi = "50"
# db.session.add(Status(jumlah_kursi))
# db.session.commit()

no_kk = "Admin"
nama_kk = ""
kepala_keluarga = ""
db.session.add(Kartukeluarga(no_kk, nama_kk, kepala_keluarga))
db.session.commit()

username = "Admin"
password = "admin123"
role = "Admin"
nama = ""
alamat = ""
telepon = ""
wilayah = ""
lingkungan = ""
jeniskelamin = ""
hub = ""
tempat_lahir = ""
tgl_lahir = ""
tempat_baptis = ""
tgl_baptis = ""
tempat_kopertama = ""
gereja_kopertama = ""
tgl_kopertama = ""
tempat_penguatan = ""
gereja_penguatan = ""
tgl_penguatan = ""
tempat_menikah = ""
gereja_menikah = ""
tgl_menikah = ""
pekerjaan = ""
no_kk = "Admin"
db.session.add(User(username, password, role, nama, alamat, telepon, wilayah, lingkungan, jeniskelamin, hub, tempat_lahir, tgl_lahir, tempat_baptis, tgl_baptis, tempat_kopertama, gereja_kopertama, tgl_kopertama, tempat_penguatan, gereja_penguatan, tgl_penguatan, tempat_menikah, gereja_menikah, tgl_menikah, pekerjaan, no_kk))
db.session.commit()
