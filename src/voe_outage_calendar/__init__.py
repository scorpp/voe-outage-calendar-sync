import logging

import ical_to_gcal_sync
from anyio.streams.file import FileWriteStream
from icalendar import Calendar

from voe_outage_calendar.models import City, Outage, OutageType

logger = logging.getLogger(__name__)


async def voe_sync_outages(city: str, street: str, building: str):
    disconnections = await fetch_outages(city, street, building)

    await export_to_ical_file(disconnections)

    await export_to_google_calendar()


async def fetch_outages(city, street, building):
    from voe_outage_calendar.voe import get_disconnections

    disconnections = await get_disconnections(city, street, building)
    list(map(logger.info, disconnections))
    return disconnections


async def export_to_google_calendar():
    import voe_outage_calendar.ica_to_gcal_sync_config

    logger.info("Syncing to Google Calendar")
    ical_to_gcal_sync.run_sync(vars(ica_to_gcal_sync_config))


async def export_to_ical_file(disconnections):
    from voe_outage_calendar.ical import write_disconnections_ical

    logger.info("Exporting outages calendar")
    async with await FileWriteStream.from_path("calendar.ics") as stream:
        await write_disconnections_ical(stream, disconnections)


def export_to_ical(outages: list[Outage]) -> Calendar:
    from voe_outage_calendar.ical import disconnections_to_ical

    return disconnections_to_ical(outages)
