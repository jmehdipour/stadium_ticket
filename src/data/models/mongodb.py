from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField, LongField, EmbeddedDocument, \
    ListField, EmbeddedDocumentField, FloatField


class User(Document):
    id = LongField(primary_key=True)
    email = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    full_name = StringField(max_length=100)
    disabled = BooleanField(default=False)
    type = IntField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)


class SeatCategory(EmbeddedDocument):
    name = StringField(required=True)
    number_of_seats = IntField(min_value=1)


class Stadium(Document):
    id = LongField(primary_key=True)
    name = StringField(required=True, unique=True)
    city = StringField(max_length=100)
    seat_categories = ListField(EmbeddedDocumentField(SeatCategory))
    sales_participation = FloatField(required=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)
