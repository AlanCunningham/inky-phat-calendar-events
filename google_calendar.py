from datetime import datetime, timezone, timedelta
import pytz
import os.path
import settings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_todays_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob"
            )

            auth_uri, _ = flow.authorization_url()
            print(f"Please visit {auth_uri} on your local computer")

            # The user will get an authorization code. This code is used to get the
            # access token.
            code = input("Enter the authorization code: ")
            flow.fetch_token(code=code)

            creds = flow.credentials

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        local_timezone = pytz.timezone("Europe/London")
        now = datetime.now(tz=local_timezone)
        tomorrow = now + timedelta(days=1)
        end_of_day = (
            datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00).isoformat()
            + "Z"
        )
        print("Getting today's events")
        events_result = (
            service.events()
            .list(
                calendarId=settings.calendar_id,
                timeMin=now.isoformat(),
                timeMax=end_of_day,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Return only today's events
        local_timezone = pytz.timezone("Europe/London")
        now = datetime.now(tz=local_timezone)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)

        all_day_events = []
        timed_events = []

        for event in events:
            if "dateTime" in event["start"]:
                event_datetime = datetime.fromisoformat(event["start"]["dateTime"])
                if event_datetime < tomorrow:
                    event_time = datetime.strftime(event_datetime, "%H:%M")
                    timed_events.append((event_time, event["summary"]))
            else:
                # All day events
                all_day_events.append(event["summary"])

        print(all_day_events)
        print(timed_events)

        return all_day_events, timed_events

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    get_todays_events()
