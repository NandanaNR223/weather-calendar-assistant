import os.path
from datetime import datetime, timezone, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("calendar", "v3", credentials=creds)

def get_calendar_events():
    service = get_calendar_service()

    now = datetime.now(timezone.utc)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end_of_day.isoformat(),
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    calendar_events = []

    for event in events:
        activity = event.get("summary", "No title")
        start = event["start"].get("dateTime", event["start"].get("date"))

        if "T" not in start:
            continue

        event_datetime = datetime.fromisoformat(start)
        event_time = event_datetime.strftime("%H:%M")

        calendar_events.append({
            "activity" : activity,
            "time" : event_time
        })

    return calendar_events
    
if __name__ == "__main__":
    print("Calendar API file is running...")
    events = get_calendar_events()

    for event in events:
        print(event["activity"])
        print(event["time"])
        print()