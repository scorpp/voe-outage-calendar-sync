from pprint import pprint
from typing import TypedDict

from django.conf import settings
from django.utils.functional import cached_property
from ical_to_gcal_sync import auth_with_calendar_api

from voe_outage_calendar import ica_to_gcal_sync_config
from voe_outage_calendar.models import Address


class GoogleCalendar(TypedDict):
    kind: str
    etag: str
    id: str
    summary: str
    description: str
    location: str
    timeZone: str


class GoogleCalendarService:
    def create_calendar(self, address: Address) -> GoogleCalendar:
        # calendar_list = self.list_calendars()
        # for calendar in calendar_list:
        #     if self.has_events(calendar["id"]):
        #         print("Can access calendar:")
        #         pprint(calendar)
        #         print("---")
        calendar = (
            self._gcal_service.calendars()
            .insert(
                body={
                    "summary": f"{address.building.name}, {address.street.name}, {address.city.name} - відключеення світла",
                    "description": "Графік відключень світла",
                    "location": "Ukraine",
                    "timeZone": settings.TIME_ZONE,
                }
            )
            .execute()
        )

        return calendar

    def list_calendars(self) -> list:
        page_token = None
        # assume all available calendars will fit into a single page :-P
        calendar_list = (
            self._gcal_service.calendarList()
            .list(maxResults=250, minAccessRole="writer", pageToken=page_token)
            .execute()
            .get("items", [])
        )
        pprint(calendar_list)
        return []

    def has_events(self, calendar_id: str) -> bool:
        events = self._gcal_service.events().list(calendarId=calendar_id, maxResults=1).execute().get("items", [])
        return bool(events)

    @cached_property
    def _gcal_service(self):
        return auth_with_calendar_api(vars(ica_to_gcal_sync_config))
