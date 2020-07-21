from django.urls import path
from users.views import UserPrivateProfilePageView, UserPublicProfilePageView
#from .views import #insertviewname


urlpatterns = [
    path('', UserPrivateProfilePageView.as_view(), name='userprofile_private_view'),
    path('public', UserPublicProfilePageView.as_view(), name='userprofile_public_view'),
]
