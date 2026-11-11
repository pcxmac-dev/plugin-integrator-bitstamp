"""What the plugin attaches to (plugin API 2.2, liminal_libs.sources.apis): Bitstamp's HTTP API v2, for its OHLC data,
and its WebSocket API v2, for the live trades. Every address below was read on Bitstamp's own pages on 2026-11-11 (the
HTTP API's page embeds its OpenAPI 3.0.3 specification, 90 paths in 18 groups, and renders an anchor for each; the
WebSocket page read in a browser, as it refuses automated readers; the status page by its title). Nothing is asked to
show it."""
from __future__ import annotations

from liminal_libs.sources.apis import Api, Area, Call, Link

VERIFIED = "2026-11-11"
HTTP_NAME = "Bitstamp HTTP API v2"
WS_NAME = "Bitstamp WebSocket API v2"
SITE = "https://www.bitstamp.net"
API_PAGE = f"{SITE}/api/"
WS_PAGE = f"{SITE}/websocket/v2/"
LEGAL = Link("Legal and privacy (terms)", f"{SITE}/legal/", "terms")
STATUS = Link("Bitstamp status", "https://status.bitstamp.net", "status")


def op(tag: str, operation: str) -> str:
    """An operation's anchor on the HTTP API's page, as the page renders it."""
    return f"{API_PAGE}#tag/{tag}/operation/{operation}"


TICKERS = "Tickers"
BOOK = "Order book"
PUBLIC_TX = "Transactions public"
MARKET_INFO = "Market info"
TRAVEL_PUBLIC = "Travel rule public"
BALANCES = "Account balances"
FEES = "Fees"
ORDERS = "Orders"
DERIVATIVES = "Derivatives"
WITHDRAWALS = "Withdrawals"
DEPOSITS = "Deposits"
SUB_ACCOUNT = "Sub account"
CONVERT = "Instant convert"
WS_TOKEN = "Websocket"
PRIVATE_TX = "Transactions private"
TRAVEL_PRIVATE = "Travel rule private"
EARN = "Earn"
SECURITY = "Security"

HTTP = Api(
    name=HTTP_NAME,
    maker="Bitstamp (Bitstamp by Robinhood)",
    about=("Bitstamp's HTTP API: its public market data (tickers, order books, trades, markets, OHLC, funding rates) "
           "without a key, and with a signed key an account's balances, fees, orders, derivatives positions, deposits "
           "and withdrawals, sub-accounts, earn and travel rule data. JSON over HTTPS."),
    kind="rest",
    base=SITE,
    version="v2 (its OpenAPI 3.0.3 specification; changelog to 2026-10-29)",
    auth=("none for the public data; private calls are signed with an API key (the X-Auth, X-Auth-Signature, "
          "X-Auth-Nonce, X-Auth-Timestamp and X-Auth-Version headers)"),
    limits=("400 requests a second for every client, and a default threshold of 10,000 requests per 10 minutes (raised "
            "by a bespoke agreement); an OHLC request answers 1,000 candles at most. Commercial use of its exchange "
            "data needs Bitstamp's commercial Data License Agreement"),
    costs=("the market data costs nothing; orders carry trading fees and withdrawals withdrawal fees (its fee "
           "schedule; none of it asked here)"),
    links=(
        Link("HTTP API documentation and reference", API_PAGE, "docs"),
        Link("Authentication", f"{API_PAGE}#section/Authentication", "auth"),
        Link("Request limits", f"{API_PAGE}#section/Request-limits", "limits"),
        Link("Changelog", f"{API_PAGE}#section/Changelog", "changelog"),
        Link("Fee schedule", f"{SITE}/fee-schedule/", "pricing"),
        STATUS,
        Link("FIX v2", f"{SITE}/fix/v2/", "docs"),
        LEGAL,
    ),
    areas=(
        Area(TICKERS, "the currencies, every market's ticker, a market's ticker and hourly ticker (public)",
             f"{API_PAGE}#tag/Tickers"),
        Area(BOOK, "a market's order book (public)", f"{API_PAGE}#tag/Order-book"),
        Area(PUBLIC_TX, "a market's latest trades (public)", f"{API_PAGE}#tag/Transactions-public"),
        Area(MARKET_INFO, "the markets, OHLC data, the EUR/USD rate, funding rates and their history (public)",
             f"{API_PAGE}#tag/Market-info", covered="OHLC data: minute bars, 1,000 a request"),
        Area(TRAVEL_PUBLIC, "the list of virtual asset service providers (public)", f"{API_PAGE}#tag/Travel-rule-public"),
        Area(BALANCES, "the account's balances, by currency", f"{API_PAGE}#tag/Account-balances"),
        Area(FEES, "trading fees and withdrawal fees", f"{API_PAGE}#tag/Fees"),
        Area(ORDERS, "limit, market and instant orders, their status, cancelling, replacing, open orders, gap "
                     "recovery", f"{API_PAGE}#tag/Orders"),
        Area(DERIVATIVES, "positions, their history and settlements, margin, collateral, leverage, market hours",
             f"{API_PAGE}#tag/Derivatives"),
        Area(WITHDRAWALS, "crypto and bank withdrawals, their status and cancelling", f"{API_PAGE}#tag/Withdrawals"),
        Area(DEPOSITS, "deposit addresses and unconfirmed deposits", f"{API_PAGE}#tag/Deposits"),
        Area(SUB_ACCOUNT, "transfers between the main account and its sub-accounts", f"{API_PAGE}#tag/Sub-account"),
        Area(CONVERT, "instant convert addresses", f"{API_PAGE}#tag/Instant-convert"),
        Area(WS_TOKEN, "the token private WebSocket channels subscribe with", f"{API_PAGE}#tag/Websocket"),
        Area(PRIVATE_TX, "the account's transactions and crypto transactions", f"{API_PAGE}#tag/Transactions-private"),
        Area(TRAVEL_PRIVATE, "travel rule contacts, counterparties, satoshi tests, xpub registrations",
             f"{API_PAGE}#tag/Travel-rule-private"),
        Area(EARN, "staking and lending subscriptions and their transactions", f"{API_PAGE}#tag/Earn"),
        Area(SECURITY, "revoking every API key", f"{API_PAGE}#tag/Security"),
    ),
    calls=(
        Call("GET /api/v2/ohlc/{market_symbol}/", "a market's OHLC data: step (seconds), limit (1 to 1,000), start or "
             "end", MARKET_INFO, used="minute bars (and 5 minutes, an hour, a day), 1,000 a request",
             docs=op("Market-info", "GetOHLCData")),
        Call("GET /api/v2/currencies/", "every currency", TICKERS, docs=op("Tickers", "GetCurrencies")),
        Call("GET /api/v2/ticker/", "every market's ticker", TICKERS, docs=op("Tickers", "GetCurrencyPairTickers")),
        Call("GET /api/v2/ticker/{market_symbol}/", "a market's ticker", TICKERS, docs=op("Tickers", "GetMarketTicker")),
        Call("GET /api/v2/ticker_hour/{market_symbol}/", "a market's hourly ticker", TICKERS,
             docs=op("Tickers", "GetHourlyCurrencyPairTicker")),
        Call("GET /api/v2/order_book/{market_symbol}/", "a market's order book", BOOK, docs=op("Order-book", "GetOrderBook")),
        Call("GET /api/v2/transactions/{market_symbol}/", "a market's latest trades", PUBLIC_TX,
             docs=op("Transactions-public", "GetTransactions")),
        Call("GET /api/v2/markets/", "every market and its details", MARKET_INFO, docs=op("Market-info", "GetMarkets")),
        Call("GET /api/v2/eur_usd/", "the EUR/USD conversion rate", MARKET_INFO,
             docs=op("Market-info", "GetEURUSDConversionRate")),
        Call("GET /api/v2/funding_rate/{market_symbol}/", "a perpetual market's funding rate", MARKET_INFO,
             docs=op("Market-info", "GetFundingRate")),
        Call("GET /api/v2/funding_rate_history/{market_symbol}/", "its funding rate history", MARKET_INFO,
             docs=op("Market-info", "GetFundingRateHistory")),
        Call("GET /api/v2/travel_rule/vasps/", "the virtual asset service providers", TRAVEL_PUBLIC,
             docs=op("Travel-rule-public", "VaspList")),
        Call("POST /api/v2/account_balances/", "the account's balances", BALANCES,
             docs=op("Account-balances", "GetAccountBalances")),
        Call("POST /api/v2/fees/trading/", "the account's trading fees", FEES, docs=op("Fees", "GetAllTradingFees")),
        Call("POST /api/v2/open_orders/", "the open orders", ORDERS, docs=op("Orders", "GetAllOpenOrders")),
        Call("POST /api/v2/order_data/", "public order events, to recover a stream's gap", ORDERS,
             docs=op("Orders", "OrderData")),
        Call("POST /api/v2/buy/{market_symbol}/", "places a limit buy order", ORDERS,
             docs=op("Orders", "OpenLimitBuyOrder"), writes=True, costs=True),
        Call("POST /api/v2/buy/market/{market_symbol}/", "places a market buy order", ORDERS,
             docs=op("Orders", "OpenMarketBuyOrder"), writes=True, costs=True),
        Call("POST /api/v2/sell/{market_symbol}/", "places a limit sell order", ORDERS,
             docs=op("Orders", "OpenLimitSellOrder"), writes=True, costs=True),
        Call("POST /api/v2/cancel_order/", "cancels an order", ORDERS, docs=op("Orders", "CancelOrder"), writes=True),
        Call("GET /api/v2/open_positions/", "the open derivatives positions", DERIVATIVES,
             docs=op("Derivatives", "GetOpenPositionList")),
        Call("GET /api/v2/margin_info/", "the account's margin", DERIVATIVES, docs=op("Derivatives", "GetMarginInfo")),
        Call("POST /api/v2/{currency}_withdrawal/", "withdraws a crypto currency", WITHDRAWALS,
             docs=op("Withdrawals", "RequestCryptoWithdrawal"), writes=True, costs=True),
        Call("POST /api/v2/{currency}_address/", "a crypto deposit address", DEPOSITS,
             docs=op("Deposits", "GetCryptoDepositAddress")),
        Call("POST /api/v2/transfer-to-main/", "moves a sub-account's balance to the main account", SUB_ACCOUNT,
             docs=op("Sub-account", "TransferFromSubToMain"), writes=True),
        Call("POST /api/v2/instant_convert_address/new/", "a new instant convert address", CONVERT,
             docs=op("Instant-convert", "RequestNewLiquidationAddress"), writes=True),
        Call("POST /api/v2/websockets_token/", "a token for the private WebSocket channels (valid 60 seconds)", WS_TOKEN,
             docs=op("Websocket", "GetWebsocketToken")),
        Call("POST /api/v2/user_transactions/", "the account's transactions", PRIVATE_TX,
             docs=op("Transactions-private", "GetUserTransactions")),
        Call("GET /api/v2/travel_rule/contacts/", "the travel rule contacts", TRAVEL_PRIVATE,
             docs=op("Travel-rule-private", "GetAllContacts")),
        Call("POST /api/v2/earn/subscribe/", "subscribes to staking or lending", EARN, docs=op("Earn", "EarnSubscribe"),
             writes=True),
        Call("POST /api/v2/revoke_all_api_keys/", "revokes every API key of the account", SECURITY,
             docs=op("Security", "RevokeAllAPIKeys"), writes=True),
    ),
    verified=VERIFIED,
)

LIVE_TRADES = "Live trades"
LIVE_ORDERS = "Live orders"
BOOKS = "Order books (order_book, detail_order_book, diff_order_book)"
FUNDING = "Live funding rate"
ANNOUNCEMENTS = "Announcements"
PRIVATE = "Private channels"
CONNECTION = "Connection, heartbeat and reconnection"

WS = Api(
    name=WS_NAME,
    maker="Bitstamp (Bitstamp by Robinhood)",
    about=("Bitstamp's real-time data over a WebSocket: subscribe to channels by market (live trades, live orders, "
           "order books, funding rates, announcements) and read their events; private channels (an account's orders, "
           "trades, settlements, liquidations) subscribe with a token from the HTTP API."),
    kind="stream",
    base="wss://ws.bitstamp.net",
    version="the WebSocket API v2",
    auth="none for the public channels; a private channel's subscribe carries a token from the HTTP API (valid 60 "
         "seconds, for one subscribing)",
    limits=("1,024 channel subscriptions a connection (the 1,025th closes it silently); client messages under 512 "
            "bytes; a connection lives 90 days at most; bts:request_reconnect gives a few seconds to reconnect"),
    costs="",
    links=(
        Link("WebSocket API v2", WS_PAGE, "docs"),
        Link("Websockets token (HTTP API)", op("Websocket", "GetWebsocketToken"), "auth"),
        STATUS,
        LEGAL,
    ),
    areas=(
        Area(LIVE_TRADES, "live_trades_[market]: every trade (id, amount, price, type, microtimestamp)", WS_PAGE,
             covered="the live trades of the coins open on a chart (live_trades_btcusd ...), one tick a trade"),
        Area(LIVE_ORDERS, "live_orders_[market]: every order created, changed or deleted, with gap detection", WS_PAGE),
        Area(BOOKS, "the top 100 levels as snapshots, with order ids, or the full book's changes", WS_PAGE),
        Area(FUNDING, "funding_rate_[market]: a perpetual's funding rate, mark and index price", WS_PAGE),
        Area(ANNOUNCEMENTS, "tokenized securities' trading halts, corporate actions and multiplier updates", WS_PAGE),
        Area(PRIVATE, "an account's orders, trades, settlements, self-trades, order trades, liquidations, token "
                      "settlements (a token each)", WS_PAGE),
        Area(CONNECTION, "bts:subscribe and bts:unsubscribe with their confirmations, bts:heartbeat, "
                         "bts:request_reconnect, bts:error", WS_PAGE,
             covered="subscribe and unsubscribe (their confirmations read: the pairs it streams), a heartbeat kept, "
                     "a reconnect when asked, an error ends the connection"),
    ),
    calls=(
        Call("bts:subscribe live_trades_[market]", "a market's trades", LIVE_TRADES,
             used="the live trades of the coins open on a chart", docs=WS_PAGE),
        Call("bts:unsubscribe live_trades_[market]", "takes a market's trades off the connection", LIVE_TRADES,
             used="a coin's chart closed: its pair off the stream", docs=WS_PAGE),
        Call("bts:heartbeat", "asks the server whether it answers", CONNECTION, used="the connection kept alive",
             docs=WS_PAGE),
        Call("bts:subscribe live_orders_[market]", "a market's order events", LIVE_ORDERS, docs=WS_PAGE),
        Call("bts:subscribe order_book_[market]", "the top 100 levels of a market's book", BOOKS, docs=WS_PAGE),
        Call("bts:subscribe detail_order_book_[market]", "the top 100 levels with each order's id", BOOKS, docs=WS_PAGE),
        Call("bts:subscribe diff_order_book_[market]", "the full book's changed levels", BOOKS, docs=WS_PAGE),
        Call("bts:subscribe funding_rate_[market]", "a perpetual's funding rate", FUNDING, docs=WS_PAGE),
        Call("bts:subscribe announcements", "tokenized securities' announcements", ANNOUNCEMENTS, docs=WS_PAGE),
        Call("bts:subscribe private-my_orders_[market]-[userId]", "the account's orders (a token)", PRIVATE, docs=WS_PAGE),
        Call("bts:subscribe private-my_trades_[market]-[userId]", "the account's fills (a token)", PRIVATE, docs=WS_PAGE),
    ),
    verified=VERIFIED,
)

APIS = (HTTP, WS)
