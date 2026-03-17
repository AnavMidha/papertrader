import requests

FINNHUB_KEY = "d6rvhhhr01qpss2hpcpgd6rvhhhr01qpss2hpcq0"
FINNHUB_BASE = "https://finnhub.io/api/v1"
USD_TO_INR = 90.0

MOCK_PRICES_USD = {
    'AAPL': 213.0, 'MSFT': 415.0, 'GOOGL': 175.0, 'AMZN': 198.0,
    'NVDA': 875.0, 'META': 535.0, 'TSLA': 175.0, 'NFLX': 628.0,
    'AMD': 155.0, 'INTC': 35.0, 'ORCL': 122.0, 'CRM': 295.0,
    'ADBE': 450.0, 'PYPL': 65.0, 'UBER': 68.0, 'LYFT': 19.0,
    'SPOT': 255.0, 'SHOP': 75.0, 'SNOW': 145.0, 'PLTR': 24.0,
    'BABA': 75.0, 'DIS': 110.0, 'NIKE': 75.0, 'SBUX': 80.0,
    'COIN': 185.0, 'SQ': 65.0, 'JPM': 195.0, 'BAC': 38.0,
    'GS': 450.0, 'V': 275.0, 'MA': 455.0, 'WMT': 68.0,
    'COST': 780.0, 'TGT': 145.0,
}

DEFAULT_WATCHLIST = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'AMZN']

STOCK_LIST = [
    {'symbol': 'AAPL',  'description': 'Apple Inc'},
    {'symbol': 'MSFT',  'description': 'Microsoft Corporation'},
    {'symbol': 'GOOGL', 'description': 'Alphabet Google'},
    {'symbol': 'AMZN',  'description': 'Amazon.com Inc'},
    {'symbol': 'NVDA',  'description': 'NVIDIA Corporation'},
    {'symbol': 'META',  'description': 'Meta Platforms Facebook'},
    {'symbol': 'TSLA',  'description': 'Tesla Inc'},
    {'symbol': 'NFLX',  'description': 'Netflix Inc'},
    {'symbol': 'AMD',   'description': 'Advanced Micro Devices'},
    {'symbol': 'INTC',  'description': 'Intel Corporation'},
    {'symbol': 'ORCL',  'description': 'Oracle Corporation'},
    {'symbol': 'CRM',   'description': 'Salesforce Inc'},
    {'symbol': 'ADBE',  'description': 'Adobe Inc'},
    {'symbol': 'PYPL',  'description': 'PayPal Holdings'},
    {'symbol': 'UBER',  'description': 'Uber Technologies'},
    {'symbol': 'LYFT',  'description': 'Lyft Inc'},
    {'symbol': 'SPOT',  'description': 'Spotify Technology'},
    {'symbol': 'SHOP',  'description': 'Shopify Inc'},
    {'symbol': 'SNOW',  'description': 'Snowflake Inc'},
    {'symbol': 'PLTR',  'description': 'Palantir Technologies'},
    {'symbol': 'BABA',  'description': 'Alibaba Group'},
    {'symbol': 'DIS',   'description': 'Walt Disney Company'},
    {'symbol': 'NIKE',  'description': 'Nike Inc'},
    {'symbol': 'SBUX',  'description': 'Starbucks Corporation'},
    {'symbol': 'COIN',  'description': 'Coinbase Global'},
    {'symbol': 'SQ',    'description': 'Block Inc Square'},
    {'symbol': 'JPM',   'description': 'JPMorgan Chase'},
    {'symbol': 'BAC',   'description': 'Bank of America'},
    {'symbol': 'GS',    'description': 'Goldman Sachs'},
    {'symbol': 'V',     'description': 'Visa Inc'},
    {'symbol': 'MA',    'description': 'Mastercard Inc'},
    {'symbol': 'WMT',   'description': 'Walmart Inc'},
    {'symbol': 'COST',  'description': 'Costco Wholesale'},
    {'symbol': 'TGT',   'description': 'Target Corporation'},
]

_cache = {}


def _get_usd_to_inr():
    try:
        resp = requests.get(
            f"{FINNHUB_BASE}/forex/rates",
            params={'base': 'USD', 'token': FINNHUB_KEY},
            timeout=5,
        )
        data = resp.json()
        rate = data.get('quote', {}).get('INR')
        if rate:
            return float(rate)
    except Exception:
        pass
    return USD_TO_INR


def get_quote(symbol: str):
    sym = symbol.upper()
    try:
        resp = requests.get(
            f"{FINNHUB_BASE}/quote",
            params={'symbol': sym, 'token': FINNHUB_KEY},
            timeout=5,
        )
        data = resp.json()
        usd_price = data.get('c', 0)
        if usd_price and usd_price > 0:
            rate = _get_usd_to_inr()
            inr_price = round(usd_price * rate, 2)
            _cache[sym] = inr_price
            return {'c': inr_price, 'pc': round(data.get('pc', usd_price) * rate, 2), 'symbol': sym}
    except Exception:
        pass

    if sym in _cache:
        return {'c': _cache[sym], 'pc': _cache[sym], 'symbol': sym}

    mock_usd = MOCK_PRICES_USD.get(sym)
    if mock_usd:
        inr = round(mock_usd * USD_TO_INR, 2)
        return {'c': inr, 'pc': round(inr * 0.99, 2), 'symbol': sym}

    return None


def get_quotes(symbols):
    result = {}
    # fetch rate once for all
    rate = _get_usd_to_inr()
    for sym in symbols:
        sym = sym.upper()
        try:
            resp = requests.get(
                f"{FINNHUB_BASE}/quote",
                params={'symbol': sym, 'token': FINNHUB_KEY},
                timeout=5,
            )
            data = resp.json()
            usd_price = data.get('c', 0)
            if usd_price and usd_price > 0:
                inr_price = round(usd_price * rate, 2)
                _cache[sym] = inr_price
                result[sym] = inr_price
                continue
        except Exception:
            pass
        if sym in _cache:
            result[sym] = _cache[sym]
        elif sym in MOCK_PRICES_USD:
            result[sym] = round(MOCK_PRICES_USD[sym] * USD_TO_INR, 2)
    return result


def search_symbol(query: str):
    q = query.lower()
    return [r for r in STOCK_LIST if q in r['symbol'].lower() or q in r['description'].lower()][:8]
