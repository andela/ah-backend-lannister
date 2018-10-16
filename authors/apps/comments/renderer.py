from authors.apps.renderer import AhJSONRenderer


class CommentJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'comment'


class CommentThreadJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'thread'

class CommentHistoryJSONRenderer(AhJSONRenderer):
    object_label = 'edit-version'
