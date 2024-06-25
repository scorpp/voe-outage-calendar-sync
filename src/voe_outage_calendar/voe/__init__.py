from datetime import timedelta
from typing import Awaitable, Callable, ParamSpec, TypeVar

from cachetools.keys import hashkey
from django.core.cache import DEFAULT_CACHE_ALIAS, caches

from voe_outage_calendar.models import Building, City, Outage, Street
from voe_outage_calendar.voe.client import VoeClient

Param = ParamSpec("Param")
RetType = TypeVar("RetType")
_CACHE_TTL = timedelta(days=1).total_seconds()
_client = VoeClient()


def amemoize(ttl: float, cache: str = DEFAULT_CACHE_ALIAS, key: str = None):
    def decorator(func: Callable[Param, Awaitable[RetType]]) -> Callable[Param, Awaitable[RetType]]:
        _cache_store = caches[cache]

        async def wrapper(*args, **kwargs):
            _key = key if key else f"{func.__module__}{func.__name__}({hash(hashkey(*args, **kwargs))})"
            if _cache_store.has_key(_key):
                return _cache_store.get(_key)

            _value = await func(*args, **kwargs)
            _cache_store.set(_key, _value, timeout=ttl)
            return _value

        return wrapper

    return decorator


@amemoize(_CACHE_TTL)
async def _get_city(city: str) -> City:
    _city, *_ = await _client.find_cities(city)
    return _city


@amemoize(_CACHE_TTL)
async def _get_street(_city: City, street: str) -> Street:
    _street, *_ = await _client.find_streets(_city, street)
    return _street


@amemoize(_CACHE_TTL)
async def _get_building(_street: Street, building: str) -> Building:
    _building, *_ = await _client.find_buildings(_street, building)
    return _building


async def get_disconnections(city: str, street: str, building: str) -> list[Outage]:
    _city = await _get_city(city)
    _street = await _get_street(_city, street)
    _building = await _get_building(_street, building)
    return await _client.get_outages(_city, _street, _building)
