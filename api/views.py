import json
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
# Create your views here.

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googlecalendar import settings

SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']


REDIRECT_URL = 'http://127.0.0.1:8000/api/v1/calendar/redirect/'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

# class api_home(View):
#     def get(sefl,request):
#         return HttpResponse("<h1>Hello</h1>")

class GoogleCalendarInitView(View):
    def get(self,request):
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URL
        authorization_url, state = flow.authorization_url(access_type='offline',prompt='consent')
        
        request.session['state'] = state
        # print(state)

        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self,request):
        state = request.session.get('state')

        if state is None:
            return HttpResponseRedirect({"error":"State Parameter missing"})
        
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,SCOPES,state=state
        )
        flow.redirect_uri = REDIRECT_URL
        

        # authorization_response = request.build_absolute_uri(reverse('calendar_redirect'))

        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        # flow.fetch_token(auth_response)

        credentials = flow.credentials

        # if 'credentials' not in request.session:
        #     print('hekko')
        #     return redirect('v1/calendar/init')
        
        service = build(API_SERVICE_NAME,API_VERSION,credentials=credentials)

        # calendar_lists = service.calendarList().list().execute()

        events_result = service.events().list(calendarId='primary',orderBy='updated',
                                              maxResults=10).execute()

        if not events_result['items']:
            print('no event')
            return HttpResponse('<h1>no event</h1>')

        events = events_result.get('items')
        print(len(events))
        final = []
        for event in events:
            temp = {}
            temp['date'] = event['start']
            temp['summary'] = event['summary']
            try: 
                temp['location']= event['location']
            except:
                temp['location'] = None
            final.append(temp)
            final.append('<br>')

        return HttpResponse(final)