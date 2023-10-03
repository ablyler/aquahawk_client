import json

import aiohttp
import pytest_asyncio
from aquahawk_client import AquaHawkClient
from aquahawk_types import Usage


@pytest_asyncio.fixture
async def client(aiohttp_client):
    app = aiohttp.web.Application()
    app.router.add_post(
        "/login", lambda request: aiohttp.web.json_response({"authenticated": True})
    )

    # Load the JSON data from the file
    with open("test_usage.json", "r") as f:
        usage_data = json.load(f)

    app.router.add_get(
        "/timeseries", lambda request: aiohttp.web.json_response(usage_data)
    )
    return app


@pytest_asyncio.fixture
async def aquahawkClient(aiohttp_client, client):
    httpClient = await aiohttp_client(client)
    return AquaHawkClient(
        "xxxx-xxxx", httpClient.host, "username", "password", httpClient, "http"
    )


async def test_get_usage_today(aquahawkClient):
    usage = await aquahawkClient.get_usage_today()
    assert isinstance(usage, Usage)
    assert usage.timeseries[10].water_use.gallons == 3.36623


async def test_get_usage_this_year(aiohttp_server, aquahawkClient):
    usage = await aquahawkClient.get_usage_this_year()
    assert isinstance(usage, Usage)
    assert usage.timeseries[10].water_use.gallons == 3.36623


async def test_authenticate(aiohttp_server, aquahawkClient):
    await aquahawkClient.authenticate()
