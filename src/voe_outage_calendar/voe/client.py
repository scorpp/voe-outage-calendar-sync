import logging
from typing import Type

import requests

from voe_outage_calendar.models import Building, City, Outage, Street
from voe_outage_calendar.voe.parsers import T, VoeAutocompleteParser, VoeOutageCalendarParser

logger = logging.getLogger(__name__)


class VoeClient:
    def __init__(self):
        self.session = requests.Session()

    def find_cities(self, city: str) -> list[City]:
        return self._get_autocomplete("https://voe.com.ua/disconnection/detailed/autocomplete/read_city", city, City)

    def find_streets(self, city: City, street: str) -> list[Street]:
        return self._get_autocomplete(
            f"https://voe.com.ua/disconnection/detailed/autocomplete/read_street/{city.id}", street, Street
        )

    def find_buildings(self, street: Street, building: str) -> list[Building]:
        return self._get_autocomplete(
            f"https://voe.com.ua/disconnection/detailed/autocomplete/read_house/{street.id}", building, Building
        )

    def get_outages(self, city: City, street: Street, building: Building) -> list[Outage]:
        calendar_html = self._get_outages_calendar_html(city, street, building)
        return VoeOutageCalendarParser().parse(calendar_html)

    def _get_autocomplete(self, url: str, q: str, model_class: Type[T]) -> list[T]:
        """Send request to autocomplete endpoint and parse the response."""
        json = self.session.get(url, params={"q": q}).json()

        parser = VoeAutocompleteParser(model_class)
        return list(map(lambda entry: parser.parse(entry["label"]), json))

    def _get_outages_calendar_html(self, city: City, street: Street, building: Building) -> str:
        resp_dict = requests.post(
            "https://voe.com.ua/disconnection/detailed?ajax_form=1&_wrapper_format=drupal_ajax&_wrapper_format=drupal_ajax",
            data={
                "city_id": city.id,
                "street_id": street.id,
                "house_id": building.id,
                "form_id": "disconnection_detailed_search_form",
            },
        ).json()
        resp_dict = filter(lambda entry: entry.get("command") == "insert", resp_dict)
        resp_dict = next(resp_dict, None)
        # TODO better error handling
        if not resp_dict:
            logger.error("No 'insert' command in API response")
        calendar_html = resp_dict.get("data")
        if not calendar_html:
            logger.error("No calendar HTML in API response")

        return calendar_html
