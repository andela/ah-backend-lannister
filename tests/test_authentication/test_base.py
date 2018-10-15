from authors.apps.articles.models import Category

class BaseTest:
    """
    Class contains data to be used for testing
    """

    def __init__(self):
        self.username = "simon"
        self.email = "simon@andela.com"
        self.password = "Simon123@"
        self.bio = "I am left handed"
        self.image_url = "https://i.stack.imgur.com/xHWG8.jpg"
        self.title = "How to tnnrain your flywwwwwwwwwwf"
        self.description = "Ever wondner how toddddd ddddwwwwd?"
        self.body = "You have to benlieve becausedddddddddcf"

        self.category = Category.objects.create(
          title='test category',
        )
        

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

        self.user_password_reset_data = {
            'user': {
                'password': self.password,
            }
        }
        self.create_article = {
            "article": {
                "title": self.title,
                "description": self.description,
                "body": self.body,
                "tags": ["reactjs"],
                
                "category": self.category.id
                
            }
        }

        self.create_article_several_tags = {
            "article": {
                "title": self.title,
                "description": self.description,
                "body": self.body,
                "tags": ["reactjs", "angularjs", "dragons"],
                "category": self.category.id
                
            }
        }

        
        self.empty_create_article = {
            "article": {
                "title": "",
                "description": "",
                "body": "",
                "tags": ["reactjs", "angularjs", "dragons"],
                 "category": self.category.id
                
            }
        }
        self.wrong_article_update = {
            "article": {
                "title": "beattr",
                "description": "",
                "body": "You cc",
                "tags": ["reactjs", "angularjs", "dragons"],
                "category": self.category.id
                
            }
        }
        
        self.update_article = {
            "article": {
                "title": "beattr",
                "description": "How to manage carrying",
                "body": "You cc",
                "tags": ["reactjs", "angularjs", "dragons"],
                "category": self.category.id
            }
        }

        self.test_comment = {
            "comment": {

                "body": "iidtfygubbbhjgfhtimes",
            }
        }
        self.test_comment_edited = {
            "comment": {

                "body": "this is edited",
            }
        }
        self.slug = 'how-to-tnnrain-your-flywwwwwwwwwwf'
        self.rate_data = {
            "rate": {
                "rating": 2,
            }
        }
        self.like_data = {
            "like": {
                "likes": True,
            }
        }

   
