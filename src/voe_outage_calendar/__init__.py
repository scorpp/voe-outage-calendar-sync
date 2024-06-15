import logging
import sys
from argparse import ArgumentParser

import ical_to_gcal_sync

import voe_outage_calendar.ica_to_gcal_sync_config
from voe_outage_calendar.ical import write_disconnections_ical
from voe_outage_calendar.voe import get_disconnections

logger = logging.getLogger(__name__)


def voe_sync_outages(city: str, street: str, building: str):
    logger.info("Fetching outages")
    disconnections = get_disconnections(city, street, building)
    list(map(logger.info, disconnections))

    logger.info("Exporting outages calendar")
    with open("calendar.ics", "wb") as f:
        write_disconnections_ical(f, disconnections)

    logger.info("Syncing to Google Calendar")
    ical_to_gcal_sync.run_sync(vars(ica_to_gcal_sync_config))


def main():
    parser = ArgumentParser("voe-crawler", description="Export Vinnytsia Oblenergo outages to Google Calendar")
    parser.add_argument("-c", "--city", help="City (Vinnytska oblast only)", required=True)
    parser.add_argument("-s", "--street", help="Street", required=True)
    parser.add_argument("-b", "--building", help="Building number", required=True)
    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("{asctime} {levelname:5} {name}: {message}", style="{"))
    logging.getLogger().addHandler(handler)
    logging.getLogger("ical_to_gcal_sync").setLevel(logging.DEBUG)
    logging.getLogger("voe_outage_calendar").setLevel(logging.DEBUG)

    voe_sync_outages(args.city, args.street, args.building)
