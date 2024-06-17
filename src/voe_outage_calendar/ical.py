from typing import IO, Iterable

from anyio.abc import ByteSendStream
from icalendar import Calendar, Event, vDatetime

from voe_outage_calendar.models import Outage


async def write_disconnections_ical(file_like: ByteSendStream, disconnections: Iterable[Outage]) -> None:
    calendar = disconnections_to_ical(disconnections)
    await file_like.send(calendar.to_ical())


def disconnections_to_ical(disconnections: Iterable[Outage]) -> Calendar:
    calendar = Calendar()
    calendar["uid"] = "c89eb9f3-262b-4306-b947-610f1ae6cbb7"
    calendar["prodid"] = "-//VOE Calendar Sync//scorpp//"
    # calendar["name"] = ""   # TODO
    for disconnect in disconnections:
        event = Event()
        event["uid"] = disconnect.id()
        event["summary"] = disconnect.status
        event["dtstart"] = vDatetime(disconnect.start)
        event["dtend"] = vDatetime(disconnect.end)
        calendar.add_component(event)

    return calendar
