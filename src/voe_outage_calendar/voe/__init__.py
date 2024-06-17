from voe_outage_calendar.models import Outage
from voe_outage_calendar.voe.client import VoeClient


async def get_disconnections(city: str, street: str, building: str) -> list[Outage]:
    _client = VoeClient()
    _city, *_ = await _client.find_cities(city)
    _street, *_ = await _client.find_streets(_city, street)
    _building, *_ = await _client.find_buildings(_street, building)
    return await _client.get_outages(_city, _street, _building)
