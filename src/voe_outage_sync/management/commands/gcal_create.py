from pprint import pformat

from django.core.management import BaseCommand

from voe_outage_calendar.models import Address, Building, City, Street
from voe_outage_sync.services.calendar import GoogleCalendarService


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-c", "--city", help="City (Vinnytska oblast only)", required=True)
        parser.add_argument("-s", "--street", help="Street", required=True)
        parser.add_argument("-b", "--building", help="Building number", required=True)

    def handle(self, *args, city: str, street: str, building: str, **options):
        address = Address(City(id=-1, name=city), Street(id=-1, name=street), Building(id=-1, name=building))
        gcal = GoogleCalendarService().create_calendar(address)
        self.stdout.write(self.style.SUCCESS("Successfully created Google Calendar"))
        self.stdout.write(self.style.SUCCESS(pformat(gcal)))
