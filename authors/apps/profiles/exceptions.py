from rest_framework.exceptions import APIException

class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = "The profile you are trying to retrieve doesnot exist"