import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from django.apps import AppConfig
from django.conf import settings

from voe_outage_calendar import voe_sync_outages

logger = logging.getLogger(__name__)


class VoeOutageSyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "voe_outage_sync"

    def ready(self):
        from voe_outage_calendar.ica_to_gcal_sync_config import CLIENT_SECRET_FILE, CREDENTIAL_PATH

        if settings.GOOGLE_CLIENT_SECRET_JSON and settings.GOOGLE_CREDENTIALS_JSON:
            with open(CLIENT_SECRET_FILE, "w") as f:
                f.write(settings.GOOGLE_CLIENT_SECRET_JSON)
            with open(CREDENTIAL_PATH, "w") as f:
                f.write(settings.GOOGLE_CREDENTIALS_JSON)

        # trick to avoid double initialisation in Django runserver with auto-reload
        if os.environ.get("RUN_MAIN", None) != "true":
            asyncio.create_task(self.run_scheduler())

    async def run_scheduler(self):
        cron_expr = settings.SYNC_RUN_CRONTAB
        values = cron_expr.split()
        if len(values) != 6:
            raise ValueError("Wrong number of fields; got {}, expected 6".format(len(values)))

        trigger = CronTrigger(
            second=values[0],
            minute=values[1],
            hour=values[2],
            day=values[3],
            month=values[4],
            day_of_week=values[5],
            timezone=settings.TIME_ZONE,
        )

        logger.debug("Initializing scheduler")

        scheduler = AsyncIOScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_job(self.sync_outages, trigger)
        await scheduler.start()  # this actually blocks

    async def sync_outages(self):
        await voe_sync_outages(os.getenv("CITY"), os.getenv("STREET"), os.getenv("BUILDING"))
