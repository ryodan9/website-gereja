from app import db, User

username = "Admin"
password = "admin123"
role = "Admin"
db.session.add(User(username, password, role))
db.session.commit()