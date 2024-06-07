import datetime
import logging
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

from voe_outage_calendar.models import Disconnection, DisconnectionEnum

logger = logging.getLogger(__name__)
TIME_ZONE = ZoneInfo("Europe/Kiev")


def get_disconnections(city, street, building) -> list[Disconnection]:
    calendar_html = send_disconnections_request(
        city_id=city,
        street_id=street,
        house_id=building,
    )

    return parse_disconnections(calendar_html)


def parse_disconnections(calendar_html: str) -> list[Disconnection]:
    time_range_axis = []
    date_axis = []
    disconnections = []

    bs = BeautifulSoup(calendar_html, "html.parser")
    today = datetime.date.today()
    slot_number = None
    col_date = None

    def parse_time(time_str: str, _date: datetime.date) -> datetime:
        _time = datetime.time.fromisoformat(time_str)
        return datetime.datetime.combine(_date, _time).replace(tzinfo=TIME_ZONE)

    for cell in bs.find_all("div", class_="disconnection-detailed-table-cell"):
        if "legend" in cell["class"] and not cell.string:
            continue  # empty top left cell

        if "head" in cell["class"]:
            time_range_axis.append(str(cell.string))

        if "day_col" in cell["class"]:
            date_axis.append(str(cell.string))
            tmp_date = str(cell.string)
            col_date = datetime.datetime.strptime(tmp_date[-5:], "%d.%m").date().replace(year=today.year)
            slot_number = 0

        if "has_disconnection" in cell["class"]:
            if "confirm_1" in cell["class"]:
                status = DisconnectionEnum.CONFIRMED
            elif "confirm_0" in cell["class"]:
                status = DisconnectionEnum.UNCONFIRMED
            else:
                status = None
                logger.warning("Cannot determine disconnection status %s", cell["class"])
            time_str = time_range_axis[slot_number]
            start_time = parse_time(time_str, col_date)
            disconnections.append(Disconnection(start_time, start_time + datetime.timedelta(hours=1), status))

        if "no_disconnection" in cell["class"] or "has_disconnection" in cell["class"]:
            slot_number += 1

    return disconnections


def send_disconnections_request(city_id, street_id, house_id) -> str:
    resp_dict = requests.post(
        "https://voe.com.ua/disconnection/detailed?ajax_form=1&_wrapper_format=drupal_ajax&_wrapper_format=drupal_ajax",
        data={
            "city_id": city_id,
            "street_id": street_id,
            "house_id": house_id,
            "form_id": "disconnection_detailed_search_form",
        },
    ).json()
    resp_dict = filter(lambda entry: entry.get("command") == "insert", resp_dict)
    resp_dict = next(resp_dict, None)
    if not resp_dict:
        logger.error("No 'insert' command in API response")
    calendar_html = resp_dict.get("data")
    if not calendar_html:
        logger.error("No calendar HTML in API response")

    return calendar_html
