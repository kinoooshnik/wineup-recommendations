from app import db, User

# probably this is all wrong and I`ll need to use requests

db.create_all()
# db.create_all(app = create_app()) # alternatively you can use this line
admin = User(username="admin", email="admin@example.com")
guest = User(username="guest", email="guest@example.com")

# adding object to a session so that we can access it later
db.session.add(admin)
db.session.add(guest)
db.session.commit()
print(User.query.all())
print(User.query.filter_by(username="admin").first())
