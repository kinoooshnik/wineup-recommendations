from peewee import *
from playhouse.db_url import connect

db = connect("sqlite:///db/default.db")


class BaseModel(Model):
    class Meta:
        database = db


class Wine(BaseModel):
    internal_id = IntegerField(null=True)
    all_names = CharField(null=True)

    def __str__(self):
        return f"Wine(id: {self.get_id()}, internal_id: {self.internal_id}, all_names: {self.all_names})"


class User(BaseModel):
    internal_id = IntegerField(null=True)

    def __str__(self):
        return f"User(id: {self.get_id()}, internal_id: {self.internal_id})"


class Review(BaseModel):
    rating = IntegerField()
    variants = IntegerField()

    wine = ForeignKeyField(Wine, backref="users_review")
    user = ForeignKeyField(User, backref="wine_reviews")

    def __str__(self):
        return f"Review(id: {self.get_id()}, rating: {self.rating}, variants: {self.variants}, wine: {self.wine}, user: {self.user})"


def create_tables():
    with db:
        db.create_tables([Wine, User, Review])
