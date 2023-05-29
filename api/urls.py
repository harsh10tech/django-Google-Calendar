from django.urls import path

from . import views

urlpatterns = [
    # path('',views.api_home.as_view()),
    path('v1/calendar/init/', views.GoogleCalendarInitView.as_view()),
    path('v1/calendar/redirect/',views.GoogleCalendarRedirectView.as_view(),name='calendar_redirect'),
]