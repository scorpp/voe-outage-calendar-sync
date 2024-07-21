LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "format": "{asctime} {levelname:5} {name}: {message}",
            "style": "{",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "ical_to_gcal_sync": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
        "voe_outage_calendar": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
        "voe_outage_sync": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
        "voe_outage_web": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        # "httpx": {"level": "DEBUG"},
        # "httpcore": {"level": "DEBUG"},
    },
}
