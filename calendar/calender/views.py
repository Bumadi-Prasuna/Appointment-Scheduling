from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import redirect,render
from datetime import timedelta
from django.http import JsonResponse
from django.http import HttpResponseRedirect


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
import google.oauth2.credentials
import google_auth_oauthlib.flow

@api_view(http_method_names=['GET'])
def build_service(request,email):
    global email_id
    email_id="prasunareddy1604@gmail.com"
    creds = None
    if os.path.exists('token.pickle_prasunareddy1604@gmail.com'):
        with open('token.pickle_prasunareddy1604@gmail.com', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/gmail.send'])
            flow.redirect_uri ="https://be45672e1287.ngrok.io/calender/oauth2callback"
            authorization_url, state = flow.authorization_url( access_type='offline', include_granted_scopes='true',login_hint=email)
            return HttpResponseRedirect(authorization_url)
    html = "<html><body><p> Thank you! </p></body></html>"
    return HttpResponse(html)


@api_view(http_method_names=['GET'])
def g_auth_endpoint(request):
    print("inside call back!!!!!")
    state = request.GET.get('state',None)
    code = request.GET.get('code',None)
    print("state:",state)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',scopes=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/gmail.send'],state=state)
    authorization_response = request.build_absolute_uri()   
    print("auth resp",authorization_response)     
    flow.redirect_uri ="https://be45672e1287.ngrok.io/calender/oauth2callback"
    #now turn those parameters into a token.
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open('token.pickle_'+email_id, 'wb') as token:
        pickle.dump(creds, token)
    print("credentials",creds)
    html = "<html><body> Thank you! </body></html>"
    return HttpResponse(html)




@api_view(http_method_names=['GET'])
def list_events(request):   
    calendar_id=request.data["calendar_id"] 
    with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    list=[]
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print("now",now)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                    maxResults=30, singleEvents=True,
                                    orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        list.append(start)
        list.append(event['id'])
    return JsonResponse(list,safe=False)

    

import pytz


@api_view(http_method_names=['GET'])
def create_event(request,email,start):
   
    with open('token.pickle_prasunareddy1604@gmail.com', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    start_datetime = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end_datetime = datetime.datetime.utcnow()+timedelta(minutes=15)
    end_datetime=end_datetime.isoformat() + 'Z' # 'Z' indicates UTC time
    start_datetime=parser.parse(start);
    end_datetime=start_datetime+timedelta(minutes=30);
    print("enddatetime")
    print(end_datetime)
    end=str(end_datetime)
    end=end.replace(" ","T")
    print("end")
    print(end)
    event={
            "summary": "Appointment fixed",
            "description": "Your appointment is fixed with .Please find the schedule",
            "start": { "dateTime":start,
                        "timeZone": "Asia/Kolkata"
                    }  ,

            "end":{"dateTime":end,
            "timeZone": "Asia/Kolkata"
                    } ,
            
                "attendees": [
                {"email":email}
                      
                
                         ],
             

            "conferenceDataVersion":1
        }      
    event = service.events().insert(calendarId="primary", body=event,sendNotifications=True).execute()
    id=event.get('id')
    print(id)
 
    return JsonResponse(event)
    
from email.mime.text import MIMEText   
import base64

@api_view(http_method_names=['GET'])
def send_email(request,email):

	with open('token.pickle_prasunareddy1604@gmail.com', 'rb') as token:
	    creds = pickle.load(token)
	service = build('gmail', 'v1', credentials=creds)	
	message = MIMEText(open("msg.txt").read())	
	message['to'] = email
	message['from'] = "prasunareddy1604@gmail.com"
	message['subject'] = "Order placed!"	
	body = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
	
	message = service.users().messages().send(userId="prasunareddy1604@gmail.com",body=body).execute()
	return JsonResponse(message)
	
@api_view(http_method_names=['GET'])
def send_otp(request,email,otp):

	with open('token.pickle_prasunareddy1604@gmail.com', 'rb') as token:
	    creds = pickle.load(token)
	service = build('gmail', 'v1', credentials=creds)
	file1 = open("otp.txt","w")
	L = ["The verification code is "+otp] 
	 
	file1.writelines(L)
	file1.close() #to change file access modes	
	message = MIMEText(open("otp.txt").read())	
	message['to'] = email
	message['from'] = "prasunareddy1604@gmail.com"
	message['subject'] = "BitsianMart OTP Verification"	
	body = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
	
	message = service.users().messages().send(userId="prasunareddy1604@gmail.com",body=body).execute()
	return JsonResponse(message)
	
@api_view(http_method_names=['PATCH'])
def create_meet(request,eventId):
    with open('token.pickle_exhub', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    
    eventPatch = request.data
     

    event = service.events().patch(
    calendarId="primary",
    eventId= eventId,
    body= eventPatch,
    sendNotifications=True,
    conferenceDataVersion=1
    ).execute() 
  
    
    
    return JsonResponse(event)

@api_view(http_method_names=['PATCH'])
def update_event(request,eventId):
    with open('token.pickle_exhub', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    event=request.data
    event = service.events().patch(calendarId='primary',eventId=eventId, body=event).execute()
    id=event.get('id')
    print(id)
 
    return JsonResponse(event)



@api_view(http_method_names=['DELETE'])
def delete_event(request):
    with open('token.pickle_exhub', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    eventId = request.POST["eventId"]
    calendarId=request.POST["calendarId"]
    event = (
        service.events()
        .delete(
            calendarId=calendarId,
            eventId=eventId
                )
        .execute()
    )
    html = "<html><body> Event Deleted! </body></html>"
    return HttpResponse(html)



 # calendarId="CALENDARID@group.calendar.google.com",


@api_view(http_method_names=['GET'])
def freeorbusy(request):
    with open('token.pickle_exhub', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    body=request.data
    response = service.freebusy().query(body=body).execute()
    return JsonResponse(response)



@api_view(http_method_names=['GET'])
def verify(request):
    with open('token.pickle_exhub', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    visitor_id=request.data['visitor_id']
    calendarId=request.data['calendarId']
    list=[]
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    timemax = datetime.datetime.utcnow()+timedelta(minutes=15)
    timemax=timemax.isoformat() + 'Z' # 'Z' indicates UTC time
    timemin=datetime.datetime.utcnow()-timedelta(minutes=15)
    timemin=timemin.isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendarId, timeMin=timemin,timeMax=timemax,
                                     singleEvents=True,
                                    orderBy='startTime').execute()
    events = events_result.get('items', [])
   

    if not events:
        print('No upcoming events found.')
    for event in events:
        for attendee in event['attendees']:
            if(attendee['email']== visitor_id ):
                print(attendee['email'])
                return HttpResponse("<html><body> True! </body></html>") 
    return HttpResponse("<html><body> False! </body></html>")    


from dateutil import parser





from dateutil.tz import tzoffset


import datetime
@api_view(http_method_names=['POST'])
def emptyslots(request,email):
    print(request)
    print(request.data)
    suggestionChips=[]
    speech=""
    display_prompt=""
    queuedMessage=""
    disableSpeechRecognition=None
    global slot_confirmed
    global date_confirmed
    global slot_list
    global date_list
    global user_name
    global user_email
    intent_name=request.data["queryResult"]["intent"]["displayName"]
    print("intent name",intent_name)
######## GET DATES OF NEXT 7 DAYS ########
    if intent_name== "book.appointment - day":
        user_name=request.data["queryResult"]["parameters"]["any"]
        user_email=request.data["queryResult"]["parameters"]["email"]
        speech="<speak>Which day would you like to make an appointment?<speak>"
        display_prompt="Choose from these"
        date_today=datetime.datetime.now().date()
        date_list=[]
        def suffix(day):
            suffix = ""
            if 4 <= day <= 20 or 24 <= day <= 30:
                suffix = "th"
            else:
                suffix = ["st", "nd", "rd"][day % 10 - 1]
            return suffix

        for i in range(7):
            date_list.append(date_today.strftime('%-d'+suffix(date_today.day)+' %B,%Y'))
            suggestionChips.append({
                "icon": "",
                "title": date_today.strftime('%-d'+suffix(date_today.day)+' %B,%Y')
                },)
            date_today=date_today+timedelta(days=1)


######  GET SLOT TIMES FOR A DATE ########
    if intent_name== "book.appointment - day - time":
     
        speech="<speak>Which time slot would be suitable for you to book an appointment ?</speak>"
        display_prompt="Choose from these"
        date=request.data["queryResult"]["parameters"]["date"]
        
        print("date",date)
        
        date_confirmed=date[:-15]
            
        request.session['date'] = date
        with open('token.pickle_'+email, 'rb') as token:
            creds = pickle.load(token)
        service = build('calendar', 'v3', credentials=creds)
        timeMin=str(parser.parse(date))+"+04:00"
        print("timemin",timeMin)
        
#        timeMax=str(parser.parse(date)+timedelta(hours=23,minutes=59,seconds=59))+"+04:00"
        timeMin=list(timeMin)
        timeMin[10]='T'
        timeMin="".join(timeMin)
        print("timemin",timeMin) 
        busy_list=[]
        start=date[:-15]+"T00:00:00+04:00"
        end=date[:-15]+"T23:59:00+04:00"
        print(start,"date")
        print('Getting the upcoming  events')
        events_result = service.events().list(calendarId='primary', timeMin=start,timeMax=end,
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            busy_list.append(parser.parse(start).replace(tzinfo=None))
        
        print("busy list",busy_list)
    

        def slot_choices(date):
            date_time=parser.parse(date)
            print("date-time",date_time)
            if date_time.date()==datetime.datetime.now().date():
                print("inside")
                ####rounding off to next 30 min slot
                def ceil_dt(dt, delta):
                    return dt + (datetime.datetime.min - dt) % delta

                now = datetime.datetime.now()
                print(now)    
                date_time=ceil_dt(now, timedelta(minutes=30))

            else:
                date_time=date[:-15]+"T00:00:00"
                date_time=parser.parse(date_time)
                


            print("datetime",date_time)
            date_chosen=date_time.date()
        
    #### setting  slot time start to 9:00
            get_time=str(date_time.time())
            if(int(get_time[:2])<9):
                date_time=str(date_time)
                date_time=str(date_chosen)+"T09:00:00"
                date_time=parser.parse(date_time)
            
            get_time=str(date_time.time())  

            print("datetime",date_time)
                


            get_date=date_chosen
            slot_choices=[]
    ##### getting slot list upto 18:00 hrs  with gap of 30 mins      
            while get_date==date_chosen and get_time!="18:00:00"  :    
                slot_choices.append(date_time)
                date_time=date_time+timedelta(minutes=30)
                get_date=date_time.date()
                get_time=str(date_time.time())
                print("date",get_date)
                print("time",get_time)    
            return list(slot_choices)

    
        print("timemin",timeMin)
        slot_choices=slot_choices(timeMin)

        print("slotchoices",slot_choices)
    
        empty_list = list(set(slot_choices)-set(busy_list))
        empty_list.sort()
        slot_list=[]
        print("empty",len(empty_list),empty_list)
        suggestionChips=[]
        for slot in empty_list:
            if str(slot)[11:-3]!="13:00" and str(slot)[11:-3]!="13:30":
                slot_list.append(slot.strftime('%I:%M %P'))
                suggestionChips.append({
                        "icon": "",
                        "title":slot.strftime('%I:%M %P')
                        },)
        


        if not slot_list:
            print(date_list)
            if date_confirmed in date_list:
                date_list.remove(date_confirmed)
            speech="<speak>There are no slots available for the date chosen.Which day would you like to make an appointment?</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for date in date_list:
                suggestionChips.append({
                        "icon": "",
                        "title": date
                        },)

        print(parser.parse(date_confirmed).date())
        print(datetime.datetime.now().date())

        if parser.parse(date_confirmed).date() < datetime.datetime.now().date():
            speech="<speak>Appointment cannot be booked for a past date. Please choose another date.</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for date in date_list:
                suggestionChips.append({
                        "icon": "",
                        "title": date
                        },)


            


        
######## CONFIRM SLOT #################
    if intent_name =="book.appointment - day - time - confirm":
        speech="<speak>Would you like me to confirm the appointment ?</speak>"
        display_prompt="Would you like me to confirm the appointment ?"
        slot_confirmed=request.data["queryResult"]["parameters"]["time"]
        if len(slot_confirmed)>10:
            slot_confirmed=slot_confirmed[11:-9]        
        
        print("in confrim slot:",slot_confirmed)
        print(slot_list)
        suggestionChips= [
    {
      "color": "#E57266",
      "icon": "https://settings.mitrarobot.com/media/icons8-checkmark-60.png",
      "title": "Yes"
    },
    {
      "icon": "https://settings.mitrarobot.com/media/icons8-delete-60.png",
      "color": "#8BD5E0",
      "title": "No"
    }
  ]

        if parser.parse(slot_confirmed).strftime('%I:%M %P') not in slot_list:
            print(parser.parse(slot_confirmed).strftime('%I:%M %P'))
            print("not in list ")
            speech="<speak>The selected time slot is not available. Please choose another time slot to book an appointment</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for slot in slot_list:
                suggestionChips.append({
                        "icon": "",
                        "title": slot
                        },)

       
########### CONFIRM SLOT AND ADD EVENT ###############
    if intent_name =="book.appointment - day - time - confirm - yes":
        speech="<speak>Your appointment has been successfully confirmed. Thank you.</speak>"
        display_prompt="Appointment confirmed!Details of the appointment are mailed to your registered email adress"
        queuedMessage="book.appointment - day - time - confirm - yes - mail"
        with open('token.pickle2', 'rb') as token:
            creds = pickle.load(token)
        service = build('calendar', 'v3', credentials=creds)
        print("date",date_confirmed)
        print("slot",slot_confirmed)
        slot_confirmed=parser.parse(slot_confirmed).strftime('%H:%M')
        
        start_datetime=date_confirmed+"T"+slot_confirmed+":00+04:00"
        print("start time:",start_datetime)
  

        end_datetime = str(parser.parse(start_datetime)+timedelta(minutes=30))
        end_datetime=list(end_datetime)
        end_datetime[10]='T'
        end_datetime="".join(end_datetime) 
        print("end",end_datetime)
        

        calendarId="primary"
        summary="appointment fixed"
        description="some description"
        body={
            "summary": "Appointment fixed",
            "description": "Your appointment is fixed with "+user_name+".Please find the schedule",
            "start": { "dateTime":start_datetime,
                        "timeZone": "Asia/Dubai"
                    }  ,

            "end":{"dateTime":end_datetime,
            "timeZone": "Asia/Dubai"
                    } ,
            
                "attendees": [
                {"email":email},
                {"email":user_email}
             
                
                         ],
             

            "conferenceDataVersion":1
        }               
        event = service.events().insert(calendarId='primary', body=body,sendUpdates="all").execute()
    

########### SEND  DIALOGFLOW TYPE  RESPONSE   ##########     

    response={
            "fulfillmentText":"",
            "fulfillmentMessages": [{

                "type": 4,
                "payload": {
                    "speech":speech,
                    "queuedMessage":queuedMessage,
                    "display_prompt":display_prompt,
                    "suggestionChips": suggestionChips,
                    "disableSpeechRecognition":disableSpeechRecognition,
                    "view":"standard"
                        }
        }]
          }
    return JsonResponse(response,safe=False)

    
    
@api_view(http_method_names=['GET'])
def confirmslot(request,slot):
    try:
        slot=parser.parse(slot)
        end_slot=slot+timedelta(minutes=30)
       
    except:
     
        slot=str(slot)
        word_list=slot.split()
        last=word_list[-1]
        slot=slot[:slot.rfind(',')]
      
        if(last=="midnight"):
            slot=parser.parse(str(slot))
            end_slot=slot+timedelta(minutes=30)
            
            
        elif(last=="noon"):
            slot=parser.parse(str(slot))+timedelta(hours=12)
            end_slot=slot+timedelta(minutes=30)

    finally:       
        slot=str(slot)
        end_slot=str(end_slot)
        slot=list(slot)
        end_slot=list(end_slot)
        slot[10]='T'
        end_slot[10]='T'
        slot="".join(slot)
        end_slot="".join(end_slot)    

    with open('token.pickle_'+email, 'rb') as token:
        creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    body={
                "summary": "Appointment fixed",
                "description": "Your appointment is fixed with  someone.Please find the schedule",
                "start": { "dateTime":slot,
                            "timeZone": "Asia/Dubai"
}  ,

                "end":{"dateTime":end_slot,
                "timeZone": "Asia/Dubai"
} ,
                
                 "attendees": [
                    {"email": ""}
                  
                    
                ],
                "conferenceDataVersion":1
             
 
 }
               
              

        
    event = service.events().insert(calendarId='primary', body=body,sendNotifications=True).execute()
    html = "<html><body><h2> Appointment slot booking was successfull!</h2><h2> An email with all the  details has been sent to your email adress .</h2></body></html>"
    return HttpResponse(html)
 
#    return JsonResponse(event)



@api_view(http_method_names=['POST'])
def create_calendar(request,CalendarName):
    with open('token.pickle2', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    calendar = {
        'summary': CalendarName,
        'timeZone': 'Asia/Kolkata'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    return JsonResponse(created_calendar)


    

@api_view(http_method_names=['GET'])
def list_calendars(request):
    with open('token.pickle2', 'rb') as token:
        creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list().execute()
    
    return JsonResponse(calendar_list)


@api_view(http_method_names=['POST'])
def create_event_calendar(request):
    calendar_summary=request.POST["calendar"]
    start_time=request.POST["start_time"] #"2020-12-15T17:30:00.047935"
    end_time=request.POST["end_time"]
    attendee=request.POST["email"]
    with open('token.pickle2', 'rb') as token:
        creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list().execute()
    for calendar in calendar_list['items']:
        if calendar["summary"]== "TestCalendar":
            calendar_id=calendar["id"]

    event={
            "summary": "Appointment fixed",
            "description": "Your appointment is fixed with  someone.Please find the schedule",
            "start": { "dateTime":start_time,
                        "timeZone": "Asia/Kolkata"
}  ,

            "end":{"dateTime": end_time,
            "timeZone": "Asia/Kolkata"
} ,
            
                "attendees": [
                {"email": email}
                
                
            ],
            "conferenceDataVersion":1
            

}
    event = service.events().insert(calendarId=calendar_id, body=event,sendNotifications=True).execute()
    id=event.get('id')
    print(id)
 
    return JsonResponse(event)




@api_view(http_method_names=['POST'])
def emptyslots_calendar(request,email):
    print(request)
    print(request.data)
    suggestionChips=[]
    speech=""
    display_prompt=""
    queuedMessage=""
    disableSpeechRecognition=None
    global slot_confirmed
    global date_confirmed
    global slot_list
    global date_list
    global user_name
    global user_email
    global calendar_id
    intent_name=request.data["queryResult"]["intent"]["displayName"]
    print("intent name",intent_name)
######## GET DATES OF NEXT 7 DAYS ########
    if intent_name== "book.appointment - day":
        user_name=request.data["queryResult"]["parameters"]["any"]
        user_email=request.data["queryResult"]["parameters"]["email"]
        speech="<speak>Which day would you like to make an appointment?<speak>"
        display_prompt="Choose from these"
        date_today=datetime.datetime.now().date()
        date_list=[]
        def suffix(day):
            suffix = ""
            if 4 <= day <= 20 or 24 <= day <= 30:
                suffix = "th"
            else:
                suffix = ["st", "nd", "rd"][day % 10 - 1]
            return suffix

        for i in range(7):
            date_list.append(date_today.strftime('%-d'+suffix(date_today.day)+' %B,%Y'))
            suggestionChips.append({
                "icon": "",
                "title": date_today.strftime('%-d'+suffix(date_today.day)+' %B,%Y')
                },)
            date_today=date_today+timedelta(days=1)


######  GET SLOT TIMES FOR A DATE ########
    if intent_name== "book.appointment - day - time":
     
        speech="<speak>Which time slot would be suitable for you to book an appointment ?</speak>"
        display_prompt="Choose from these"
        date=request.data["queryResult"]["parameters"]["date"]
        
        print("date",date)
        
        date_confirmed=date[:-15]
            
        request.session['date'] = date
        with open('token.pickle2', 'rb') as token:
            creds = pickle.load(token)
        service = build('calendar', 'v3', credentials=creds)
        calendar_list = service.calendarList().list().execute()
        for calendar in calendar_list['items']:
            if calendar["summary"]== user_email:
                calendar_id=calendar["id"]
        timeMin=str(parser.parse(date))+"+04:00"
        print("timemin",timeMin)
        
#        timeMax=str(parser.parse(date)+timedelta(hours=23,minutes=59,seconds=59))+"+04:00"
        timeMin=list(timeMin)
        timeMin[10]='T'
        timeMin="".join(timeMin)
        print("timemin",timeMin) 
        busy_list=[]
        start=date[:-15]+"T00:00:00+04:00"
        end=date[:-15]+"T23:59:00+04:00"
        print(start,"date")
        print('Getting the upcoming  events')
        events_result = service.events().list(calendarId=calendar_id, timeMin=start,timeMax=end,
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
           
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            busy_list.append(parser.parse(start).replace(tzinfo=None))
        
        print("busy list",busy_list)
    

        def slot_choices(date):
            date_time=parser.parse(date)
            print("date-time",date_time)
            if date_time.date()==datetime.datetime.now().date():
                print("inside")
                ####rounding off to next 30 min slot
                def ceil_dt(dt, delta):
                    return dt + (datetime.datetime.min - dt) % delta

                now = datetime.datetime.now()
                print(now)    
                date_time=ceil_dt(now, timedelta(minutes=30))

            else:
                date_time=date[:-15]+"T00:00:00"
                date_time=parser.parse(date_time)
                


            print("datetime",date_time)
            date_chosen=date_time.date()
        
    #### setting  slot time start to 9:00
            get_time=str(date_time.time())
            if(int(get_time[:2])<9):
                date_time=str(date_time)
                date_time=str(date_chosen)+"T09:00:00"
                date_time=parser.parse(date_time)
            
            get_time=str(date_time.time())  

            print("datetime",date_time)
                


            get_date=date_chosen
            slot_choices=[]
    ##### getting slot list upto 18:00 hrs  with gap of 30 mins      
            while get_date==date_chosen and get_time!="18:00:00"  :    
                slot_choices.append(date_time)
                date_time=date_time+timedelta(minutes=30)
                get_date=date_time.date()
                get_time=str(date_time.time())
                print("date",get_date)
                print("time",get_time)    
            return list(slot_choices)

    
        print("timemin",timeMin)
        slot_choices=slot_choices(timeMin)

        print("slotchoices",slot_choices)
    
        empty_list = list(set(slot_choices)-set(busy_list))
        empty_list.sort()
        slot_list=[]
        print("empty",len(empty_list),empty_list)
        suggestionChips=[]
        for slot in empty_list:
            if str(slot)[11:-3]!="13:00" and str(slot)[11:-3]!="13:30":
                slot_list.append(slot.strftime('%I:%M %P'))
                suggestionChips.append({
                        "icon": "",
                        "title":slot.strftime('%I:%M %P')
                        },)
        


        if not slot_list:
            print(date_list)
            if date_confirmed in date_list:
                date_list.remove(date_confirmed)
            speech="<speak>There are no slots available for the date chosen.Which day would you like to make an appointment?</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for date in date_list:
                suggestionChips.append({
                        "icon": "",
                        "title": date
                        },)

        print(parser.parse(date_confirmed).date())
        print(datetime.datetime.now().date())

        if parser.parse(date_confirmed).date() < datetime.datetime.now().date():
            speech="<speak>Appointment cannot be booked for a past date. Please choose another date.</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for date in date_list:
                suggestionChips.append({
                        "icon": "",
                        "title": date
                        },)


            


        
######## CONFIRM SLOT #################
    if intent_name =="book.appointment - day - time - confirm":
        speech="<speak>Would you like me to confirm the appointment ?</speak>"
        display_prompt="Would you like me to confirm the appointment ?"
        slot_confirmed=request.data["queryResult"]["parameters"]["time"]
        if len(slot_confirmed)>10:
            slot_confirmed=slot_confirmed[11:-9]        
        
        print("in confrim slot:",slot_confirmed)
        print(slot_list)
        suggestionChips= [
    {
      "color": "#E57266",
      "icon": "https://settings.mitrarobot.com/media/icons8-checkmark-60.png",
      "title": "Yes"
    },
    {
      "icon": "https://settings.mitrarobot.com/media/icons8-delete-60.png",
      "color": "#8BD5E0",
      "title": "No"
    }
  ]

        if parser.parse(slot_confirmed).strftime('%I:%M %P') not in slot_list:
            print(parser.parse(slot_confirmed).strftime('%I:%M %P'))
            print("not in list ")
            speech="<speak>The selected time slot is not available. Please choose another time slot to book an appointment</speak>"
            display_prompt="Choose from these"
            suggestionChips=[]
            for slot in slot_list:
                suggestionChips.append({
                        "icon": "",
                        "title": slot
                        },)

       
########### CONFIRM SLOT AND ADD EVENT ###############
    if intent_name =="book.appointment - day - time - confirm - yes":
        speech="<speak>Your appointment has been successfully confirmed. Thank you.</speak>"
        display_prompt="Appointment confirmed!Details of the appointment are mailed to your registered email adress"
        queuedMessage="book.appointment - day - time - confirm - yes - mail"
        with open('token.pickle2', 'rb') as token:
            creds = pickle.load(token)
        service = build('calendar', 'v3', credentials=creds)
        print("date",date_confirmed)
        print("slot",slot_confirmed)
        slot_confirmed=parser.parse(slot_confirmed).strftime('%H:%M')
        
        start_datetime=date_confirmed+"T"+slot_confirmed+":00+04:00"
        print("start time:",start_datetime)
  

        end_datetime = str(parser.parse(start_datetime)+timedelta(minutes=30))
        end_datetime=list(end_datetime)
        end_datetime[10]='T'
        end_datetime="".join(end_datetime) 
        print("end",end_datetime)
        

        summary="appointment fixed"
        description="some description"
        body={
            "summary": "Appointment fixed",
            "description": "Your appointment is fixed with "+user_name +".Please find the schedule",
            "start": { "dateTime":start_datetime,
                        "timeZone": "Asia/Dubai"
                    }  ,

            "end":{"dateTime":end_datetime,
            "timeZone": "Asia/Dubai"
                    } ,
            
                "attendees": [
                {"email":email},
                {"email":user_email}
             
                
                         ],
             

            "conferenceDataVersion":1
        }               
        event = service.events().insert(calendarId=calendar_id, body=body,sendUpdates="all").execute()
    

########### SEND  DIALOGFLOW TYPE  RESPONSE   ##########     

    response={
            "fulfillmentText":"",
            "fulfillmentMessages": [{

                "type": 4,
                "payload": {
                    "speech":speech,
                    "queuedMessage":queuedMessage,
                    "display_prompt":display_prompt,
                    "suggestionChips": suggestionChips,
                    "disableSpeechRecognition":disableSpeechRecognition,
                    "view":"standard"
                        }
        }]
          }
    return JsonResponse(response,safe=False)

