import datetime as dt
import logging
import os
import threading
import time

from django.apps import AppConfig
from django.conf import settings
from scheduler import Scheduler

from voe_outage_calendar import voe_sync_outages

logger = logging.getLogger(__name__)


def scheduler_thread_func(scheduler: Scheduler):
    while True:
        scheduler.exec_jobs()
        time.sleep(1)


class VoeOutageSyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "voe_outage_sync"

    def ready(self):
        from voe_outage_calendar.ica_to_gcal_sync_config import CLIENT_SECRET_FILE, CREDENTIAL_PATH

        with open(CLIENT_SECRET_FILE, "w") as f:
            f.write(settings.GOOGLE_CLIENT_SECRET_JSON)
        with open(CREDENTIAL_PATH, "w") as f:
            f.write(settings.GOOGLE_CREDENTIALS_JSON)

        # trick to avoid double initialisation in Django runserver with auto-reload
        if os.environ.get("RUN_MAIN", None) != "true":
            logger.debug("Initializing scheduler")

            scheduler = Scheduler()
            scheduler.hourly(dt.time(minute=0, second=0), self.sync_outages)

            thread = threading.Thread(target=scheduler_thread_func, args=(scheduler,), daemon=True)
            thread.start()

    def sync_outages(self):
        voe_sync_outages(os.getenv("CITY"), os.getenv("STREET"), os.getenv("BUILDING"))
