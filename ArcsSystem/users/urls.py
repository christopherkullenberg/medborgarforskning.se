from django.urls import path
from users.views import UserPrivateProfilePageView, UserPublicProfilePageView, AcceptTermsPageView, UserEidtMyPageView
from django.views.decorators.csrf import csrf_exempt
#from .views import #insertviewname


urlpatterns = [
    # path('', UserProfilePageView.as_view(), name='userprofile_generic_view')

    path('', UserPrivateProfilePageView, name='userprofile_private_view'),
    path('edit/', UserEidtMyPageView.as_view(), name='userprofile_edit_view'),
    path('public/', UserPublicProfilePageView.as_view(), name='loggedin_userprofile_public_view'),
    path('public/<slug:username>/', UserPublicProfilePageView.as_view(), name='userprofile_public_view'),
    path('terms/', AcceptTermsPageView.as_view(), name='accept-terms'),
]
