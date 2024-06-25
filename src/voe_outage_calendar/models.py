import datetime
import hashlib
from dataclasses import dataclass
from enum import Enum, StrEnum
from django.utils.translation import gettext_lazy as _


@dataclass(eq=True, frozen=True)  # request __hash__ method generation
class IdName:
    id: int
    name: str


class City(IdName):
    pass


class Street(IdName):
    pass


class Building(IdName):
    pass


class OutageType(StrEnum):
    CONFIRMED = "confirmed", _("Confirmed")
    UNCONFIRMED = "unconfirmed", _("Unconfirmed")

    def __new__(cls, value, label):
        instance = str.__new__(cls, value)
        instance._value_ = value
        instance._label = label
        return instance

    def __str__(self):
        return str(self._label)


@dataclass
class Outage:
    start: datetime.datetime
    end: datetime.datetime
    status: OutageType

    def id(self):
        digest = hashlib.md5()
        digest.update(self.start.isoformat().encode("utf-8"))
        digest.update(self.end.isoformat().encode("utf-8"))
        digest.update(self.status.value.encode("utf-8"))
        return digest.hexdigest()

    def __str__(self):
        return f"{self.start.isoformat()} {self.end - self.start} {self.status}"
