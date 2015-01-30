
from uuid import UUID

from werkzeug.routing import BaseConverter, RequestRedirect, ValidationError


class UUIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            u = UUID(value)
        except ValueError:
            raise ValidationError()

        if str(u) == value:
            # the uuid is already canonical
            return u
        else:
            raise ValidationError()
            # TODO instead redirect the client to use the canonical url
            #  - this may require patching Werkzeug
            #  - or just creating my own Rule objects
            # the rule should be:
            #  if url_for('this-view', these_args) != actual_url,
            #   we should redirect

    def to_url(self, value):
        if not isinstance(value, UUID):
            raise ValidationError('expected a UUID but got: {}'.format(repr(value)), value)
        return str(value)
