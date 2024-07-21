import logging
from http import HTTPStatus

from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBase, StreamingHttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic.base import ContextMixin

from voe_outage_calendar import export_to_ical, fetch_outages

logger = logging.getLogger(__name__)


class JinjaAsyncTemplateView(ContextMixin, View):
    template_name: str

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponseBase:
        context = self.get_context_data()
        return await self.render_to_response(context)

    async def render_to_response(self, context, **response_kwargs):
        template = get_template(self.template_name)
        return StreamingHttpResponse(template.template.generate_async(context=context), **response_kwargs)


class IndexView(JinjaAsyncTemplateView):
    template_name = "index.html"


class SiteWebManifestView(JinjaAsyncTemplateView):
    template_name = "site.webmanifest"


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
