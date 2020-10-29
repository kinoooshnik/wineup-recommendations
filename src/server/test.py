from src.server.orm import User, Wine, Review, db, create_tables

create_tables()
db.connect()


# Первый способ создавать строки в БД
wine1 = Wine.create(internal_id=1, all_names="a")
wine2 = Wine.create(internal_id=None, all_names=None)
# Второй способ создавать строки в БД
wine3 = Wine(internal_id=2, all_names="n")
wine3.save()

user1 = User.create(internal_id=1)
user2 = User.create(internal_id=2)

print(*[wine for wine in Wine.select()], sep="\n")
print()
print(*[user for user in User.select()], sep="\n")
print()

review1 = Review.create(rating=4, variants=5, wine=wine1, user=user1)
review2 = Review.create(rating=3, variants=5, wine=wine2, user=user1)
review3 = Review.create(rating=5, variants=5, wine=wine3, user=user1)
review4 = Review.create(rating=5, variants=5, wine=wine1, user=user2)

print(*[wine for wine in user1.wine_reviews], sep="\n")
print()
print(*[user for user in wine1.users_review], sep="\n")
print()

db.close()
