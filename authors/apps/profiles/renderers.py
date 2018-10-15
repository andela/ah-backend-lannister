from authors.apps.renderer import AhJSONRenderer


class ProfileJSONRenderer(AhJSONRenderer):
    object_label = 'profile'
    charset = 'utf-8'
