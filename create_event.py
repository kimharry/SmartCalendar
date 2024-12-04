import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_event(event_text):
    creds = None
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())
        
    try:
        service = build("calendar", "v3", credentials=creds)

        # event_text
        # title: (이벤트의 제목)
        # start_date: (시작 날짜, 형식: YYYY-MM-DDTHH:MM:SSZ)
        # end_date: (종료 날짜, 형식: YYYY-MM-DDTHH:MM:SSZ)
        # location: (위치)
        for line in event_text.split("\n"):
            if line.startswith("title: "):
                title = line[len("title: "):]

            elif line.startswith("start_date: "):
                start_date = line[len("start_date: "):] + "+09:00"

            elif line.startswith("end_date: "):
                end_date = line[len("end_date: "):] + "+09:00"

            elif line.startswith("location: "):
                location = line[len("location: "):]

        event = {
            "summary": title,
            "location": location,
            "start": {
                "dateTime": start_date,
                "timeZone": "Asia/Seoul"
            },
            "end": {
                "dateTime": end_date,
                "timeZone": "Asia/Seoul"
            }
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    create_event("""title: 2024 RC미리메리크리스마스
start_date: 2024-11-27T18:00:00
end_date: 2024-11-27T23:00:00
location: 테슬라커뮤니티센터 및 구내 식당""")