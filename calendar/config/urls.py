
from django.conf import settings
from django.conf.urls import include, url 
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework import routers
from rest_framework.authtoken import views
from django.urls import  re_path,path
from project.users import views as mu_views

from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()

router = routers.DefaultRouter()
router.register(r'companies', mu_views.CompanyViewSet)


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # Your stuff: custom urls includes go here

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^calender/', include('calender.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    re_path(r'^$', RedirectView.as_view(url='admin/', permanent=True)),
    #url(r'^api/company/$', mu_views.get_company, name='get_company'),
    url(r'^api/company/$', (mu_views.all_visits))
    #re_path('^visits$', views.all_visits),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
