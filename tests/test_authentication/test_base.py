class BaseTest:
    """
    Class contains data to be used for testing
    """

    def __init__(self):
        self.username = "simon"
        self.email = "simon@andela.com"
        self.password = "12345678"
        self.bio = "I am left handed"
        self.image_url = "https://i.stack.imgur.com/xHWG8.jpg"
        self.reg_data = {
            "user": {
                "username": self.username,
                "email": self.email,
                "password": self.password
            }
        }
        self.user_login = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.wrong_reg_data = {
            "user": {
                "username": self.username,
                "email": None,
                "password": self.password
            }
        }

        self.update_data = {
            "user": {
                "email": self.email,
                "bio": self.bio,
                "image": self.image_url
            }
        }
        self.self_no_password_login = {
            "user": {
                "username": self.username,
                "email": self.email,
                "password": None
            }
        }
        self.no_email_login = {
            "user": {
                "username": self.username,
                "email": None,
                "password": self.password
            }
        }
