import logging
from http import HTTPStatus

from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views import View

from voe_outage_calendar import export_to_ical, fetch_outages

logger = logging.getLogger(__name__)


class IndexView(View):
    async def get(self, request):
        return HttpResponse(status=200, content_type="text/plain", content=b"VOE outages sync")


class RunSyncView(View):
    async def post(self, request: HttpRequest):
        if request.body.decode() == settings.INTERNAL_SECRET:
            await apps.get_app_config("voe_outage_sync").sync_outages()
            return HttpResponse(status=HTTPStatus.OK, content_type="text/plain", content=b"OK")

        return HttpResponse(status=HTTPStatus.FORBIDDEN, content_type="text/plain", content=b"Forbidden")


class ICalView(View):
    async def get(self, request: HttpRequest, city: str, street: str, building: str):
        logger.info("Generating ICAL for %s, %s, %s", city, street, building)
        outages = await fetch_outages(city, street, building)
        calendar = export_to_ical(outages)
        return HttpResponse(status=HTTPStatus.OK, content_type="text/calendar", content=calendar.to_ical())
