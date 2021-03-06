"""
Renderer classes go here
"""
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class AhJSONRenderer(JSONRenderer):
    """
    Override default renderer to customise output
    """
    charset = 'utf-8'
    object_label = 'object'

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
                return super(AhJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.object_label: data
            })

        else:
            return json.dumps({
                self.object_label+'s': data
            })
            