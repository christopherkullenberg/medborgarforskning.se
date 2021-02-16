from django.urls import path
from users.views import UserPrivateProfilePageView, UserPublicProfilePageView, AcceptTermsPageView
#from .views import #insertviewname

urlpatterns = [
    # path('', UserProfilePageView.as_view(), name='userprofile_generic_view'),
    path('', UserPrivateProfilePageView.as_view(), name='userprofile_private_view'),
    path('public/', UserPublicProfilePageView.as_view(), name='loggedin_userprofile_public_view'),
    path('public/<slug:display_name>/', UserPublicProfilePageView.as_view(), name='userprofile_public_view'),
    path('terms/', AcceptTermsPageView.as_view(), name='accept-terms'),
]
