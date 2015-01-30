
from mongoengine import Document, StringField


class User(Document):
    openid = StringField(required=True)  # identity url
    fullname = StringField()
    nickname = StringField()
    image_url = StringField()
    email = StringField()

    meta = {
        'indexes': [
            'openid',
        ]
    }

    @classmethod
    def get_or_create(cls, openid, fullname, nickname, image_url, email):
        cls.objects._collection.find_and_modify(
            query={ 'openid': openid },
            update={ '$set': {
                'fullname': fullname,
                'nickname': nickname,
                'image_url': image_url,
                'email': email,
            } },
            new=True,
            upsert=True,
        )
        return cls.objects(openid=openid).get()
