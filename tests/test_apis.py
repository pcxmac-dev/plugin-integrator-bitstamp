"""What the plugin attaches to (plugin API 2.2): Bitstamp's HTTP API v2 and its WebSocket API v2 as Bitstamp's pages
describe them, the calls it says it makes being the ones its source and its stream really send, what they learned
said without a request, and (LIMINAL_VENDOR_PAGES=1 only) every page it names still answering. Nothing else is sent; no
ledger or key is touched."""
from __future__ import annotations

import gc
import json
import os
import re
from datetime import datetime, timezone

import pytest

from liminal_libs.config import load_settings
from liminal_libs.sources.apis import dead_links, problems, urls
from liminal_libs.sources.http import PublicClient

import plugin_integrator_bitstamp as bitstamp
from plugin_integrator_bitstamp import BASE_URL, BitstampSource, BitstampStream
from plugin_integrator_bitstamp.apis import HTTP, HTTP_NAME, SITE, WS, WS_NAME
from plugin_integrator_bitstamp.facts import NOTES

from .conftest import FakeResponse, FakeSession
from .test_bitstamp import _ohlc

OHLC = re.compile(r"^/api/v2/ohlc/[a-z0-9]+/$")


@pytest.fixture(autouse=True)
def fresh_notes():
    NOTES.clear()
    yield
    NOTES.clear()


def _stream_calls(messages: list[str]) -> set[str]:
    """The card's names of the stream's messages: the event, and its channel with the market as [market]."""
    out = set()
    for m in map(json.loads, messages):
        channel = (m.get("data") or {}).get("channel")
        out.add(m["event"] + (" " + re.sub(r"^live_trades_[a-z0-9]+$", "live_trades_[market]", channel) if channel else ""))
    return out


def test_it_declares_both_apis_soundly_with_every_part_and_what_it_does_with_each():
    apis = bitstamp.PLUGIN.apis
    assert apis == (HTTP, WS) and problems(apis) == [] and [a.name for a in apis] == [HTTP_NAME, WS_NAME]
    assert BASE_URL == HTTP.base + "/api/v2" and WS.base == BitstampStream().url  # the cards' addresses are the plugin's
    assert HTTP.docs == "https://www.bitstamp.net/api/" and WS.docs == "https://www.bitstamp.net/websocket/v2/"
    assert len(HTTP.areas) == 18 and [a.name for a in HTTP.covered] == ["Market info"]
    assert [a.name for a in WS.covered] == ["Live trades", "Connection, heartbeat and reconnection"]
    for api in apis:
        assert {c.area for c in api.calls} <= {a.name for a in api.areas} and api.verified == "2026-11-11"
        assert not any(c.writes or c.costs for c in api.used)  # what it makes only reads
    assert {c.name for c in HTTP.calls if c.costs} >= {"POST /api/v2/buy/{market_symbol}/", "POST /api/v2/{currency}_withdrawal/"}
    assert "10,000 requests per 10 minutes" in HTTP.limits and "1,024 channel subscriptions" in WS.limits
    assert "10,000 per 10 minutes" in bitstamp.PLUGIN.limits  # the plugin's own words, as its page says now
    assert all(u.startswith("https://") for u in urls(apis))


def test_the_calls_it_says_it_makes_are_the_ones_its_source_and_its_stream_send():
    t0 = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())
    session = FakeSession([FakeResponse(200, {"data": {"ohlc": [_ohlc(t0), _ohlc(t0 + 60)]}})])
    src = BitstampSource(PublicClient(BASE_URL, session=session, sleep=lambda s: None))
    list(src.bar_pages("BTCUSD", datetime.fromtimestamp(t0, timezone.utc), datetime.fromtimestamp(t0 + 120, timezone.utc),
                       "minute", limit=2))
    paths = {url.removeprefix(SITE) for url, _, _ in session.calls}
    assert paths and all(OHLC.match(p) for p in paths)
    assert {c.name for c in HTTP.used} == {"GET /api/v2/ohlc/{market_symbol}/"}
    stream = BitstampStream(dynamic=True)
    sent = stream.subscribe(["BTC"]) + stream.change({"ETHUSD"}, {"BTCUSD"}) + [stream.keepalive]
    assert _stream_calls(sent) == {c.name for c in WS.used} == {
        "bts:subscribe live_trades_[market]", "bts:unsubscribe live_trades_[market]", "bts:heartbeat"}


def test_api_facts_say_what_its_client_and_its_stream_learned_and_ask_nothing():
    assert bitstamp.PLUGIN.api_facts() == {}  # nothing built or opened here yet: nothing known, nothing asked
    built = bitstamp.PLUGIN.build(load_settings(env={}, env_file=None), 5)  # its build notes its client (no request)
    assert bitstamp.PLUGIN.api_facts()[HTTP_NAME]["Requests"] == "0 so far (of 5 allowed)" and built.client.requests_made == 0
    stream = BitstampStream(dynamic=True)  # the recorder opens it; it notes itself
    stream.parse({"event": "bts:subscription_succeeded", "channel": "live_trades_btcusd", "data": {}})
    stream.parse({"event": "bts:subscription_succeeded", "channel": "live_trades_ethusd", "data": {}})
    stream.parse({"event": "bts:unsubscription_succeeded", "channel": "live_trades_ethusd", "data": {}})
    said = bitstamp.PLUGIN.api_facts()[WS_NAME]
    assert said["Pairs confirmed"] == "BTCUSD" and said["Stream opened"].endswith("(open)")
    del built, stream
    gc.collect()
    after = bitstamp.PLUGIN.api_facts()
    assert after[HTTP_NAME]["Run began"].endswith("(ended)") and after[WS_NAME]["Stream opened"].endswith("(closed)")


@pytest.mark.skipif(os.environ.get("LIMINAL_VENDOR_PAGES") != "1", reason="asks Bitstamp's pages: set LIMINAL_VENDOR_PAGES=1")
def test_every_page_it_names_answers():
    assert dead_links(bitstamp.PLUGIN.apis) == []
