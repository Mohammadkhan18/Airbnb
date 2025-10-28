from mongoengine import (
    Document, StringField, EmailField, DateTimeField, URLField, ListField, IntField, ReferenceField, CASCADE, EmbeddedDocumentField
)
from datetime import datetime
from django.contrib.auth.hashers import make_password

# -----------------------
# User Model
# -----------------------
class User(Document):
    meta = {'collection': 'User'}
    name = StringField(max_length=100, null=True)
    email = EmailField(unique=True, null=True)
    password = StringField(max_length=255, null=True)
    emailVerified = DateTimeField(null=True)
    image = URLField(null=True)
    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)
    favoriteIds = ListField(ReferenceField('Listing'),default=[])
    def save(self, *args, **kwargs):
        # Auto hash password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        self.updatedAt = datetime.utcnow()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email or "Unnamed User"


# -----------------------
# Account Model
# -----------------------
class Account(Document):
    userId = ReferenceField(User, reverse_delete_rule=CASCADE)
    type = StringField(max_length=50, required=True)
    provider = StringField(max_length=100, required=True)
    providerAccountId = StringField(max_length=255, required=True)
    refresh_token = StringField(null=True)
    access_token = StringField(null=True)
    expires_at = IntField(null=True)
    token_type = StringField(null=True)
    scope = StringField(null=True)
    id_token = StringField(null=True)
    session_state = StringField(null=True)

    meta = {
        'collection': 'Account',
        'indexes': [
            {'fields': ['provider', 'providerAccountId'], 'unique': True}
        ]
    }

    def __str__(self):
        return f"{self.provider} ({self.user.email})"


# -----------------------
# Listing Model
# -----------------------
class Listing(Document):
    userId = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(max_length=255, required=True)
    description = StringField(required=True)
    imageSrc = URLField(required=True)
    createdAt = DateTimeField(default=datetime.utcnow)
    category = StringField(max_length=100)
    roomCount = IntField()
    bathroomCount = IntField()
    guestCount = IntField()
    locationValue = StringField()
    price = IntField()

    meta = {
        'collection': 'Listing'
    }

    def __str__(self):
        return f"{self.title} - {self.userId.email if self.userId else 'No User'}"



# -----------------------
# Reservation Model
# -----------------------
class Reservation(Document):
    userId = ReferenceField(User, reverse_delete_rule=CASCADE)
    listingId = ReferenceField(Listing, reverse_delete_rule=CASCADE)
    startDate = DateTimeField(required=True)
    endDate = DateTimeField(required=True)
    totalPrice = IntField()
    createdAt = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'Reservation'
    }

    def __str__(self):
        return f"Reservation {self.id} by {self.userId}"
