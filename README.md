# django-Google-Calendar
In this assignment you have to implement google calendar
integration using django rest api. You need to use the OAuth2 mechanism to
get users calendar access. Below are detail of API endpoint and
corresponding views which you need to implement

A) /rest/v1/calendar/init/ -> GoogleCalendarInitView()
This view should start step 1 of the OAuth. Which will prompt user for
his/her credentials

B) /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
This view will do two things
1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar

C) [harshcode2020.pythonanywhere.com](harshcode2020.pythonanywhere.com) web-app link of the application deployed on PythonAnywhere