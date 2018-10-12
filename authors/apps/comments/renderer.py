import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                # As mentioned about, we will let the default JSONRenderer handle
                # rendering errors.
                return super(CommentJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'comment': data

        })


class CommentsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return json.dumps(data)
        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'comments': data

        })


class CommentThreadJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return json.dumps(data)
        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'thread': data

        })
