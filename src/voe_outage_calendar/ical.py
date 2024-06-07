from typing import IO, Iterable

from icalendar import Calendar, Event, vDatetime

from voe_outage_calendar.models import Disconnection


def write_disconnections_ical(file_like: IO, disconnections: Iterable[Disconnection]) -> None:
    calendar = disconnections_to_ical(disconnections)
    file_like.write(calendar.to_ical())


def disconnections_to_ical(disconnections: Iterable[Disconnection]) -> Calendar:
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
