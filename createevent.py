import datetime
import os.path
import pickle
import google.auth
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

credentials = get_credentials()
service = build('calendar', 'v3', credentials=credentials)

def create_event(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY',
        ],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


summary = input('Enter event summary: ')
start_time_str = input('Enter event start time (YYYY-MM-DD HH:MM): ')
end_time_str = input('Enter event end time (YYYY-MM-DD HH:MM): ')
start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
create_event(summary, start_time, end_time)
