"""
Renderer classes go here
"""
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class ArticleJSONRenderer(JSONRenderer):
    """
    Override default renderer to customise output
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        render response data
        :param data:
        :param accepted_media_type:
        :param renderer_context:
        :return:
        """
        if type(data) != ReturnList:
            errors = data.get('errors', None)
            if errors is not None:
                return super(ArticleJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            # single article
            return json.dumps({
                'article': data
            })

        # Finally, we can render our data under the "user" namespace.
        else:
            # many articles
            return json.dumps({
                'articles': data
            })
            
class RateUserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        if type(data) != ReturnList:
            errors = data.get('errors', None)
            if errors is not None:
                return super(RateUserJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            # single article
            return json.dumps({
                'rate': data
            })

        else:
        # Finally, we can render our data under the "article" namespace.
            return json.dumps({
                'rate': data
            
        })
        
class LikeUserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        if type(data) != ReturnList:
            errors = data.get('errors', None)
            if errors is not None:
                return super(LikeUserJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            # single article
            return json.dumps({
                'like': data
            })

        else:
        # Finally, we can render our data under the "article" namespace.
            return json.dumps({
                'like': data
            
        })