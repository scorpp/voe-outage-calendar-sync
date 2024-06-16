import datetime
import hashlib
from dataclasses import dataclass
from enum import Enum


@dataclass
class IdName:
    id: int
    name: str


class City(IdName):
    pass


class Street(IdName):
    pass


class Building(IdName):
    pass


class OutageType(str, Enum):
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"

    def __str__(self):
        return self.value


@dataclass
class Outage:
    start: datetime.datetime
    end: datetime.datetime
    status: OutageType

    def id(self):
        digest = hashlib.md5()
        digest.update(self.start.isoformat().encode("utf-8"))
        digest.update(self.end.isoformat().encode("utf-8"))
        digest.update(str(self.status).encode("utf-8"))
        return digest.hexdigest()

    def __str__(self):
        return f"{self.start.isoformat()} {self.end - self.start} {self.status}"
