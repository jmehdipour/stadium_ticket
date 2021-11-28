from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField, LongField


class User(Document):
    id = LongField(primary_key=True)
    email = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    full_name = StringField(max_length=100)
    disabled = BooleanField(default=False)
    type = IntField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)
