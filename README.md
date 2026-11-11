# plugin-integrator-bitstamp

Bitstamp for [Liminal](https://github.com/pcxmac-dev/liminal-charts): the exchange's crypto minute bars
from 2011 (its public candles API) and its public trade stream, for the coins open on a chart. No
key. An exchange of its own: its history is a market apart from the other exchanges', never closed.

A Liminal provider plugin released on its own. The app finds it through the entry point group
`liminal.providers` and lists it on the Plugins view and in `liminal-charts plugins`
as `package: plugin-integrator-bitstamp`, with this package's version.

## Its API

It attaches to two of Bitstamp's interfaces, both public and keyless for what it asks; its page in every app shows them
(`PLUGIN.apis`), with every part of each, the calls it makes among the rest, and what its client and its stream learned
(`PLUGIN.api_facts()`):

- **The HTTP API v2** ([documentation](https://www.bitstamp.net/api/)): the
  [OHLC data](https://www.bitstamp.net/api/#tag/Market-info/operation/GetOHLCData)
  (`GET /api/v2/ohlc/{market_symbol}/`, 1,000 a request) for the minute bars. Every client may make 400 requests a
  second and 10,000 per 10 minutes by default ([request limits](https://www.bitstamp.net/api/#section/Request-limits));
  commercial use of its exchange data needs Bitstamp's Data License Agreement.
- **The WebSocket API v2** ([documentation](https://www.bitstamp.net/websocket/v2/)): the `live_trades_[market]`
  channels for the coins open on a chart, and its heartbeat.
- [Fee schedule](https://www.bitstamp.net/fee-schedule/), [status](https://status.bitstamp.net),
  [legal](https://www.bitstamp.net/legal/).

## Install

Into the app's environment, from the app's folder:

```powershell
.venv\Scripts\python.exe -m pip install "plugin-integrator-bitstamp @ git+https://github.com/pcxmac-dev/plugin-integrator-bitstamp@v0.3.0"
```

or with the app's plugins (`pip install -e ".[plugins]"` in liminal-charts). The app loads it on its next
start.

## Compatibility

It is written for plugin API 2.2 (`PLUGIN.api`: the class contract, `BitstampPlugin` a
`CryptoVenuePlugin` of liminal-libs 1.49.0 or later, declaring what it attaches to, `apis`). An app offering 2.2 or a
later 2.x loads it; an app of another major, or one older than 2.2, leaves it out and says why on the Plugins view.

## Develop

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install "liminal-libs @ git+https://github.com/pcxmac-dev/liminal-libs@main"
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

Tests never send requests (a fake session answers) and never read your keys.
