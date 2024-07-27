import asyncio

from django.core.management import BaseCommand

from voe_outage_calendar import voe_sync_outages


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-c", "--city", help="City (Vinnytska oblast only)", required=True)
        parser.add_argument("-s", "--street", help="Street", required=True)
        parser.add_argument("-b", "--building", help="Building number", required=True)

    def handle(self, *args, city: str, street: str, building: str, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(voe_sync_outages(city, street, building))
        loop.close()
