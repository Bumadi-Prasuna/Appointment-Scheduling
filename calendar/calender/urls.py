
from django.conf import settings
from django.conf.urls import include, url 
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework import routers
from rest_framework.authtoken import views
from django.urls import  re_path,path
from project.users import views as mu_view

from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
  #  path('create-event/', views.create_event.urls),
  path('build/<email>', views.build_service),
  path('oauth2callback', views.g_auth_endpoint,name='auth'),
  path('list/', views.list_events,name='list'),
  path('create/<email>/<start>/', views.create_event,name='create'),
  path('send/<email>', views.send_email,name='send'),
  path('sendotp/<email>/<otp>', views.send_otp,name='send_otp'),
  path('delete/', views.delete_event,name='delete'),
  path('free/', views.freeorbusy,name='free'),
#  path('html/<slots>', views.html,name='print-html'),
  path('update/<eventId>', views.update_event),
  path('meet/<eventId>', views.create_meet),
  path('verify/', views.verify),
#  path('slotchoices/', views.slot_choices),
  path('emptyslots/<email>', views.emptyslots),
  path('confirmslot/<slot>', views.confirmslot),
  path('create_calendar/<CalendarName>', views.create_calendar),
  path('list_calendars/', views.list_calendars),
  path('create_event_calendar/', views.create_event_calendar),
  path('emptyslots_calendar/<email>', views.emptyslots_calendar),
  



#  path('build/',views.current,name='current')
]
