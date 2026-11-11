# Changelog

## 0.3.0 (2026-11-11)

Its APIs on its page (plugin API 2.2, liminal-libs 1.49.0; the user: "each plugin should reflect the the API its attached
to, and present links that provide documentation, the plugin interface should more or less contain what it already has,
BUT, it should also expose more of what the API is about"). `BitstampPlugin.apis` declares the two things it talks to,
read from Bitstamp's own pages on 2026-11-11 (`apis.py`):

- **Bitstamp's HTTP API v2** (www.bitstamp.net/api/v2): its documentation (its page embeds its OpenAPI 3.0.3
  specification), authentication, request limits, changelog, fee schedule, status page, FIX v2 and the legal pages; all
  eighteen groups of its reference, each said used or not; the one call it makes (`GET /api/v2/ohlc/{market_symbol}/`)
  among 30 others, each linked to its anchor on the page, the ones that change something or cost said so;
- **its WebSocket API v2** (ws.bitstamp.net): the page and the websockets token; its channels in seven parts; what it
  sends (`bts:subscribe` and `bts:unsubscribe` of `live_trades_[market]`, `bts:heartbeat`) beside the other channels.

Its limits in words are Bitstamp's of today: "400 requests a second; 10,000 per 10 minutes by default" (it said 8,000
per 10 minutes, Bitstamp's older figure; its window and caps are unchanged and well inside either). `api_facts()` says
what its client and its stream learned while they ran, asking nothing: the requests made, the last answer's clock, the
rate-limit headers its server sent, the pairs the stream's server confirmed (`facts.py`: each held weakly, its last
words kept when it goes; its build now notes the client it makes, the stream notes itself). Tests: the contract at 2.2,
the cards' calls the ones its source and its stream send, the facts, and every page it names answering (only with
`LIMINAL_VENDOR_PAGES=1`). On liminal-libs 1.49.0 or later.

## 0.2.0 (2026-11-03)

Renamed `plugin-integrator-bitstamp` (the package `plugin_integrator_bitstamp`; it was `liminal-plugin-bitstamp`) on 2026-11-03: the naming by system (plugins are `plugin-<app>-<name>`), on liminal-libs 1.4.0 (`liminal_libs`, the library renamed with it).

- A class on plugin API 2.0 (liminal-libs 1.3.0; the user: "all the plugins under liminal should basically
  follow inheritance/oop paradigm"): `BitstampPlugin(CryptoVenuePlugin)`, a crypto exchange's plugin of
  `liminal_libs.sources.archive` (its `assets` and `kind`; its source built on the contract's public client at
  `base_url`), what the `Provider` record declared as class attributes and its callback as a method
  (`carries`), `PLUGIN` its instance. Its `view` stays the contract's own, as the record's was: its fixed
  plan and caps, all the history it holds (`CRYPTO_VENUE_DAYS` limits Coinbase and Bitfinex, not it).
- It declares its publication delay itself (`delays`: each minute once it closes, the row the library held
  for the `bitstamp-public` plan).
- Every behaviour, limit and string as in 1.3.1. Versioned 0.2.0 with every Liminal distribution of the
  release (its `release/0.2.0` branch; CI against the library's).

## 1.3.1 (2026-11-02)

The plugin imports the library as `liminal_libs` and depends on liminal-libs (the app, renamed liminal-charts, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-charts").

## 1.3.0 (2026-11-01)

- Released as its own package, `plugin-integrator-bitstamp`, registered under the entry point group
  `liminal.providers`; its version is the distribution's.
- Its plan and request caps are in it (`TIER`, `PER_RUN`, `PER_DAY`), no longer in the app's
  `config.PUBLIC_FEEDS`.
- Plugin API 1.6.

## 1.2.0 (2026-10-31)

- Built into the app (then massive-collate): its source class, client and trade stream in its
  module (plugin API 1.6).

## 1.1.0 and 1.0.0

- Built into the app (then massive-collate); see the app's history.
