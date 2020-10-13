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
from django.conf.urls.static import static
from django.conf import settings
### Sitemap requirements start #
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
from blog.sitemaps import BlogSitemap
from organizations.sitemaps import OrganizationSitemap
from projects.sitemaps import ProjectSitemap
from publications.sitemaps import PublicationSitemap
from staticpages.sitemaps import StaticpagesSitemap
from workpackages.sitemaps import WorkPackageSitemap

### Sitemap requirements end #

# Setting the Admin Login Text - changes what is seen when logging into the backend of django admin
admin.site.site_title = _("ARCS Admin Portal") # Seen at the login form for the admin
admin.site.site_header = _("ARCS Admin") # Seen at top of admin after login to admin
admin.site.index_title = _("Welcome to the ARCS Admin Portal") # Seen at top of app list on login to admin


sitemaps = {
    'Blog': BlogSitemap,
    'Organization': OrganizationSitemap,
    'Project': ProjectSitemap,
    'Publication': PublicationSitemap,
    'Stiticpages': StaticpagesSitemap,
    # 'WorkPackage': WorkPackageSitemap
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path(_('manage-arcs/'), admin.site.urls),
    path(_('accounts/profile/'), include('users.urls')),
    path(_('accounts/'), include('allauth.urls')),
    path(_('blog/'), include('blog.urls')),
    path(_('project/'),include('projects.urls')),
#    path(_('resources/'), include('staticpages.urls')), # TODO remove - make relative sections of urls.py in staticpages use this prefix
    path(_('publications/'),include('publications.urls')),
    path(_('people/'),include('users.urls')),
    path('summernote/', include('django_summernote.urls')), # adding summernote (CK))
    path('resources/', include('workpackages.urls')),
    path(_(''), include('staticpages.urls')),
    path(_('org/'), include('organizations.urls')),
    #) # Replace line below with just a ] for production
    path(('sitemap.xml'), views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TODO only for dev. disable for production
