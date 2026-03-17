import requests

ALPHA_VANTAGE_KEY = "3R82IPUSCA445BT4"
ALPHA_BASE = "https://www.alphavantage.co/query"

MOCK_PRICES = {
    'RELIANCE.NS': 2850.00, 'TCS.NS': 2409.20, 'INFY.NS': 1249.80,
    'HDFCBANK.NS': 840.60, 'ICICIBANK.NS': 1050.00, 'SBIN.NS': 1066.70,
    'WIPRO.NS': 480.00, 'HINDUNILVR.NS': 2400.00, 'ITC.NS': 450.00,
    'BAJFINANCE.NS': 878.15, 'ADANIENT.NS': 2400.00, 'TATAMOTORS.NS': 950.00,
    'TATAPOWER.NS': 380.00, 'TATASTEEL.NS': 140.00, 'MARUTI.NS': 12500.00,
    'SUNPHARMA.NS': 1600.00, 'HCLTECH.NS': 1450.00, 'AXISBANK.NS': 1100.00,
    'KOTAKBANK.NS': 1800.00, 'LT.NS': 3500.00, 'ONGC.NS': 280.00,
    'NTPC.NS': 360.00, 'ZOMATO.NS': 220.00, 'PAYTM.NS': 340.00,
    'IRCTC.NS': 780.00, 'NYKAA.NS': 180.00, 'DMART.NS': 3800.00,
    'BAJAJFINSV.NS': 1600.00, 'ASIANPAINT.NS': 2200.00, 'NESTLEIND.NS': 2200.00,
    'TITAN.NS': 3200.00, 'ADANIPORTS.NS': 1200.00, 'HAL.NS': 4200.00,
    'BEL.NS': 280.00, 'IRFC.NS': 180.00, 'RVNL.NS': 420.00,
}

DEFAULT_WATCHLIST = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS',
    'HDFCBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS'
]

STOCK_LIST = [
    {'symbol': 'RELIANCE.NS', 'description': 'Reliance Industries'},
    {'symbol': 'TCS.NS', 'description': 'Tata Consultancy Services'},
    {'symbol': 'INFY.NS', 'description': 'Infosys Ltd'},
    {'symbol': 'HDFCBANK.NS', 'description': 'HDFC Bank'},
    {'symbol': 'ICICIBANK.NS', 'description': 'ICICI Bank'},
    {'symbol': 'SBIN.NS', 'description': 'State Bank of India'},
    {'symbol': 'WIPRO.NS', 'description': 'Wipro Ltd'},
    {'symbol': 'HINDUNILVR.NS', 'description': 'Hindustan Unilever'},
    {'symbol': 'ITC.NS', 'description': 'ITC Ltd'},
    {'symbol': 'BAJFINANCE.NS', 'description': 'Bajaj Finance'},
    {'symbol': 'ADANIENT.NS', 'description': 'Adani Enterprises'},
    {'symbol': 'TATAMOTORS.NS', 'description': 'Tata Motors'},
    {'symbol': 'TATAPOWER.NS', 'description': 'Tata Power'},
    {'symbol': 'TATASTEEL.NS', 'description': 'Tata Steel'},
    {'symbol': 'MARUTI.NS', 'description': 'Maruti Suzuki'},
    {'symbol': 'SUNPHARMA.NS', 'description': 'Sun Pharmaceutical'},
    {'symbol': 'HCLTECH.NS', 'description': 'HCL Technologies'},
    {'symbol': 'AXISBANK.NS', 'description': 'Axis Bank'},
    {'symbol': 'KOTAKBANK.NS', 'description': 'Kotak Mahindra Bank'},
    {'symbol': 'LT.NS', 'description': 'Larsen and Toubro'},
    {'symbol': 'ONGC.NS', 'description': 'Oil and Natural Gas Corp'},
    {'symbol': 'NTPC.NS', 'description': 'NTPC Ltd'},
    {'symbol': 'ZOMATO.NS', 'description': 'Zomato Ltd'},
    {'symbol': 'PAYTM.NS', 'description': 'Paytm One97 Communications'},
    {'symbol': 'IRCTC.NS', 'description': 'Indian Railway Catering IRCTC'},
    {'symbol': 'NYKAA.NS', 'description': 'FSN E-Commerce Nykaa'},
    {'symbol': 'DMART.NS', 'description': 'Avenue Supermarts DMart'},
    {'symbol': 'BAJAJFINSV.NS', 'description': 'Bajaj Finserv'},
    {'symbol': 'ASIANPAINT.NS', 'description': 'Asian Paints'},
    {'symbol': 'NESTLEIND.NS', 'description': 'Nestle India'},
    {'symbol': 'TITAN.NS', 'description': 'Titan Company'},
    {'symbol': 'ADANIPORTS.NS', 'description': 'Adani Ports'},
    {'symbol': 'HAL.NS', 'description': 'Hindustan Aeronautics HAL'},
    {'symbol': 'BEL.NS', 'description': 'Bharat Electronics BEL'},
    {'symbol': 'IRFC.NS', 'description': 'Indian Railway Finance IRFC'},
    {'symbol': 'RVNL.NS', 'description': 'Rail Vikas Nigam RVNL'},
    {'symbol': 'TRENT.NS', 'description': 'Trent Zudio Westside'},
    {'symbol': 'NAUKRI.NS', 'description': 'Info Edge Naukri'},
    {'symbol': 'HAVELLS.NS', 'description': 'Havells India'},
    {'symbol': 'DRREDDY.NS', 'description': 'Dr Reddys Laboratories'},
    {'symbol': 'CIPLA.NS', 'description': 'Cipla Ltd'},
    {'symbol': 'EICHERMOT.NS', 'description': 'Eicher Motors Royal Enfield'},
    {'symbol': 'HEROMOTOCO.NS', 'description': 'Hero MotoCorp'},
    {'symbol': 'COALINDIA.NS', 'description': 'Coal India'},
    {'symbol': 'JSWSTEEL.NS', 'description': 'JSW Steel'},
    {'symbol': 'HINDALCO.NS', 'description': 'Hindalco Industries'},
    {'symbol': 'INDUSINDBK.NS', 'description': 'IndusInd Bank'},
    {'symbol': 'PNB.NS', 'description': 'Punjab National Bank'},
    {'symbol': 'BANKBARODA.NS', 'description': 'Bank of Baroda'},
    {'symbol': 'ULTRACEMCO.NS', 'description': 'UltraTech Cement'},
    {'symbol': 'TECHM.NS', 'description': 'Tech Mahindra'},
    {'symbol': 'PIDILITIND.NS', 'description': 'Pidilite Industries Fevicol'},
    {'symbol': 'COLPAL.NS', 'description': 'Colgate Palmolive India'},
    {'symbol': 'MARICO.NS', 'description': 'Marico Ltd'},
    {'symbol': 'DABUR.NS', 'description': 'Dabur India'},
    {'symbol': 'GODREJCP.NS', 'description': 'Godrej Consumer Products'},
]

_cache = {}


def get_quote(symbol: str):
    sym = symbol.upper()
    av_symbol = sym.replace('.NS', '.BSE')
    try:
        resp = requests.get(
            ALPHA_BASE,
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': av_symbol,
                'apikey': ALPHA_VANTAGE_KEY,
            },
            timeout=10,
        )
        data = resp.json()
        quote = data.get('Global Quote', {})
        price = float(quote.get('05. price', 0))
        if price > 0:
            _cache[sym] = price
            return {'c': round(price, 2), 'pc': round(price * 0.99, 2), 'symbol': sym}
    except Exception:
        pass

    if sym in _cache:
        return {'c': _cache[sym], 'pc': _cache[sym], 'symbol': sym}

    mock = MOCK_PRICES.get(sym)
    if mock:
        return {'c': mock, 'pc': mock * 0.99, 'symbol': sym}

    return None


def get_quotes(symbols):
    result = {}
    for sym in symbols:
        q = get_quote(sym)
        if q:
            result[sym.upper()] = q['c']
    return result


def search_symbol(query: str):
    q = query.lower()
    return [r for r in STOCK_LIST if q in r['symbol'].lower() or q in r['description'].lower()][:8]
