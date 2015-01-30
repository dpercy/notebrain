
import uuid

from flask_mongoengine import Document
from mongoengine import (
    GenericReferenceField,
    ReferenceField,
    StringField,
    UUIDField
)

from .mod_auth.models import User


class Note(Document):
    id = UUIDField(primary_key=True)
    owner = ReferenceField(User, required=True)
    html = StringField(default='')

    meta = {
        'indexes': [
            ('owner', 'id'),
        ]
    }

    def clean(self):
        # Generate the id on save, rather than on construction.
        # This makes it easier to distinguish unsaved Notes.
        if self.id is None:
            self.id = uuid.uuid4()
