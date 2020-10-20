from django.urls import path
from users.views import (UserPrivateProfilePageView,
                        UserPublicProfilePageView,
                        AcceptTermsPageView,
                        UserEidtMyPageView,
                        MyProfileView,
                        UsersPublicProflieListView,)
from django.views.decorators.csrf import csrf_exempt
#from .views import #insertviewname

urlpatterns = [
    # path('', UserProfilePageView.as_view(), name='userprofile_generic_view')

    path('', UserPrivateProfilePageView, name='userprofile_private_view'),
    path('profile/', MyProfileView.as_view(), name='my_profile_view' ),
    path('profile/edit/', UserEidtMyPageView.as_view(), name='userprofile_edit_view'),
    path('users/', UsersPublicProflieListView.as_view(), name='users_list'),
    path('users/<slug:username>/', UserPublicProfilePageView.as_view(), name='userprofile_public_view'),
    path('terms/', AcceptTermsPageView.as_view(), name='accept-terms'),
]
