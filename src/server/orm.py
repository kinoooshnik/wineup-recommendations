from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "db/db.db"
db = SQLAlchemy(app)


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internal_id = db.Column(db.Integer, nullable=True)
    all_names = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Wine {self.id}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internal_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<User {self.id}>"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    variants = db.Column(db.Integer)

    wine_id = db.Column(db.Integer, db.ForeignKey("wine.id"), nullable=False)
    wine = db.relationship("Wine", backref=db.backref("reviews", lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("reviews", lazy=True))

    def __repr__(self):
        return f"<Review {self.id}>"
