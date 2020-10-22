from orm import Wine
from orm import User
from orm import Review
from orm import db

db.create_all()

wine1 = Wine(id=1, internal_id=1, all_names="a")
wine2 = Wine(id=2, internal_id=None, all_names="b")
wine3 = Wine(id=3, internal_id=3, all_names="c")

db.session.add(wine1)
db.session.add(wine2)
db.session.add(wine3)
db.session.commit()

print(Wine.query.all())

user1 = Wine(id=1, internal_id=1)
user2 = Wine(id=2, internal_id=None)
user3 = Wine(id=3, internal_id=3)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

print(User.query.all())
