from django.urls import path
from users.views import UserProfilePageView
#from .views import #insertviewname


urlpatterns = [
    path('', UserProfilePageView.as_view(), name='userprofile_generic_view')
]
