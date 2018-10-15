from django.contrib.auth.models import User
from .models import FollowingUser


def get_followed_user(user):
    """  Returns a list of users that the given user follows.   """

    userlist = FollowingUser.objects.filter(following_user=user).values_list('followed_user',
                                                                             flat=True)
    return User.objects.filter(id__in=userlist)


def get_following_user(user):
    """  Returns a list of users that follow the given user.  """

    userlist = FollowingUser.objects.filter(followed_user=user).values_list('following_user',
                                                                            flat=True)
    return User.objects.filter(id__in=userlist)


def get_following_each_other(user):
    """
    Returns a list of users that a given user follows and they follow the user back.
    """
    user_follows = FollowingUser.objects.filter(following_user=user).values_list('followed_user',
                                                                            flat=True)
    user_followed = FollowingUser.objects.filter(followed_user=user).values_list('following_user',
                                                                             flat=True)
    return User.objects.filter(
        id__in=set(user_follows).intersection(set(user_followed)))
