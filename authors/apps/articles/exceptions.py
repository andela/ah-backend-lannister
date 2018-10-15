from rest_framework.exceptions import APIException

class TagHasNoArticles(APIException):
    status_code = 400
    default_detail = "This tag currently has no articles"

class CatHasNoArticles(APIException):
    status_code = 400
    default_detail = "This category currently has no articles"