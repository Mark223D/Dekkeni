from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class UserAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return "/user/"