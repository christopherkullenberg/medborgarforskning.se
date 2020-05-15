"""arcs_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.utils.translation import gettext_lazy as _

### Wagtail requirements Start #
from django.urls import re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static
from django.conf import settings
### Wagtail requirements End #

# Setting the Admin Login Text - changes what is seen when logging into the backend of django admin
admin.site.site_title = _("ARCS Admin Portal") # Seen at the login form for the admin
admin.site.site_header = _("ARCS Admin") # Seen at top of admin after login to admin
admin.site.index_title = _("Welcome to the ARCS Admin Portal") # Seen at top of app list on login to admin


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path(_('manage-arcs/'), admin.site.urls),
    path(_('accounts/profile/'), include('users.urls')),
    path(_('accounts/'), include('allauth.urls')),
    path(_('blog/'), include('blog.urls')),
    ### Wagtail paths start #
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(_(r'^documents/'), include(wagtaildocs_urls)),
    re_path(_(r'^pages/'), include(wagtail_urls)),
    ### Wagtail paths end #
    path(_('project/'),include('projects.urls')),
#    path(_('resources/'), include('staticpages.urls')), # TODO remove - make relative sections of urls.py in staticpages use this prefix
    path(_('publications/'),include('publications.urls')),
    path(_('people/'),include('users.urls')),
    path('summernote/', include('django_summernote.urls')), # adding summernote (CK))
    path(_(''), include('staticpages.urls')),
    #) # Replace line below with just a ] for production
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TODO only for dev. disable for production
