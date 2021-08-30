from config import db

#test for database access

#db.users.insert_one({"name": "Chris", "email": "test@mail.com"})
#db.users.insert_one({"name": "Admin", "email": "admin@mail.com"})
#db.users.insert_one({"name": "Staff", "email": "staff@mail.com"})


cursor = db.users.find({"name": "Staff"})
for user in cursor:
    print(user)