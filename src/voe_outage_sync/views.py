from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request):
        return HttpResponse(status=200, content_type="text/plain", content=b"VOE outages sync")


class RunSyncView(View):
    def post(self, request: HttpRequest):
        if request.body.decode() == settings.INTERNAL_SECRET:
            apps.get_app_config("voe_outage_sync").sync_outages()
            return HttpResponse(status=200, content_type="text/plain", content=b"OK")

        return HttpResponse(status=403, content_type="text/plain", content=b"Forbidden")
