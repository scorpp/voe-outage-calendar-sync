import datetime
import logging
from typing import Type, TypeVar
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

from voe_outage_calendar.models import IdName, Outage, OutageType

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=IdName)


class VoeAutocompleteParser[T]:
    model_class: Type[T]

    def __init__(self, model_class: Type[T]) -> None:
        self.model_class = model_class

    def parse(self, html: str) -> T:
        bs = BeautifulSoup(html, "html.parser").find()
        _id = bs["data-id"]
        _name = bs.get_text()
        return self.model_class(id=_id, name=_name)


class VoeOutageCalendarParser:
    def parse(self, calendar_html: str) -> list[Outage]:
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
                    status = OutageType.CONFIRMED
                elif "confirm_0" in cell["class"]:
                    status = OutageType.UNCONFIRMED
                else:
                    status = None
                    logger.warning("Cannot determine disconnection status %s", cell["class"])
                time_str = time_range_axis[slot_number]
                start_time = parse_time(time_str, col_date)
                disconnections.append(Outage(start_time, start_time + datetime.timedelta(hours=1), status))

            if "no_disconnection" in cell["class"] or "has_disconnection" in cell["class"]:
                slot_number += 1

        return disconnections


TIME_ZONE = ZoneInfo("Europe/Kiev")
