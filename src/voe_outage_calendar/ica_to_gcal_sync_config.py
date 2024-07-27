# iCal feeds. More than one feed can be specified.
#
# 'source': The iCal feed URL for the events that should be synced to the Google Calendar.
# Note that the syncing is one-way only.
#
# 'destination': The ID of the calendar to use for iCal events, should be of the form
# 'ID@group.calendar.google.com', check the calendar settings page to find it.
# All calendars should be writable with the same google credenatials
# (can also be 'primary' to use the default calendar)
#
# 'files': If it is True then 'source' is the path to a folder full of ics files.
#
#  Feeds can be of mixed types
from voe_outage_web import settings

ICAL_FEEDS = [
    {
        "source": "./",
        "destination": "407a6503537268e7e51b3b4f369095bdecb00da6fd74fab97c20f4525bacbbc1@group.calendar.google.com",
        "files": True,
    },
]

# Authentication information for the ical feeds.
# The same credentials are used for all feeds where 'files' is False
# If the feed does not require authentication or if FILES is true, it should be left to None
ICAL_FEED_USER = None
ICAL_FEED_PASS = None

# If the iCalendar server is using a self signed ssl certificate, certificate checking must be disabled.
# This option applies to all feeds where 'files' is False
# If unsure left it to True
ICAL_FEED_VERIFY_SSL_CERT = True

# Must use the OAuth scope that allows write access
# TODO need to make it a list https://github.com/scorpp/voe-outage-calendar-sync/issues/1
# SCOPES = "https://www.googleapis.com/auth/calendar.calendarlist.readonly https://www.googleapis.com/auth/calendar.app.created"
SCOPES = "https://www.googleapis.com/auth/calendar.app.created"

# API secret stored in this file
CLIENT_SECRET_FILE = "/tmp/ical_to_gcal_sync_client_secret.json"

# Location to store API credentials
CREDENTIAL_PATH = "/tmp/ical_to_gcal_sync_credentials.json"

# Application name for the Google Calendar API
APPLICATION_NAME = "ical_to_gcal_sync"

# File to use for logging output
LOGFILE = None  #'ical_to_gcal_sync.log'

# Time to pause between successive API calls that may trigger rate-limiting protection
API_SLEEP_TIME = 0.10

# Integer value >= 0
# Controls the timespan within which events from ICAL_FEED will be processed
# by the script.
#
# For example, setting a value of 14 would sync all events from the current
# date+time up to a point 14 days in the future.
#
# If you want to sync all events available from the feed this is also possible
# by setting the value to 0, *BUT* be aware that due to an API limitation in the
# icalevents module which prevents an open-ended timespan being used, this will
# actually be equivalent to "all events up to a year from now" (to sync events
# further into the future than that, set a sufficiently high number of days).
ICAL_DAYS_TO_SYNC = 0

# Integer value >= 0
# Controls how many days in the past to query/update from Google and the ical source.
# If you want to only worry about today's events and future events, set to 0,
# otherwise set to a positive number (e.g. 30) to include that many days in the past.
# Any events outside of that time-range will be untouched in the Google Calendar.
# If the ical source doesn't include historical events, then this will mean deleting
# a rolling number of days historical calendar entries from Google Calendar as the script
# runs
PAST_DAYS_TO_SYNC = 30

# Restore deleted events
# If this is set to True, then events that have been deleted from the Google Calendar
# will be restored by this script - otherwise they will be left deleted, but will
# be updated - just Google won't show them
RESTORE_DELETED_EVENTS = True

# function to modify events coming from the ical source before they get compared
# to the Google Calendar entries and inserted/deleted
#
# this function should modify the events in-place and return either True (keep) or
# False (delete/skip) the event from the Calendar. If this returns False on an event
# that is already in the Google Calendar, the event will be deleted from the Google
# Calendar
import icalevents


def EVENT_PREPROCESSOR(ev: icalevents.icalparser.Event) -> bool:
    # include all entries by default
    # see README.md for examples of rules that make changes/skip
    return True


# Sometimes you can encounter an annoying situation where events have been fully deleted
# (by manually emptying the "Bin" for the calendar), but attempting to add new events with
# the same UIDs will continue to fail. Inserts will produce a 409 "already exists" error,
# and updtes will produce a 403 "Forbidden" error. Probably because the events are still
# stored somewhere even though they are no longer visible to the API or through the web
# interface.
#
# If you run into this situation and don't want to create a fresh calendar, you can try
# setting this value to something other than an empty string. It will be used as a prefix
# for new event UIDs, so changing it from the default will prevent the same IDs from being
# reused and allow them to be inserted as normal.
#
# NOTE: Characters allowed in the ID are those used in base32hex encoding, i.e. lowercase
# letters a-v and digits 0-9, see section 3.1.2 in RFC2938
EVENT_ID_PREFIX = ""
