import yfinance as yf

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
    {'symbol': 'BAJFINANCE.NS', 'description': 'Tata Motors'},
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
    {'symbol': 'BRITANNIA.NS', 'description': 'Britannia Industries'},
    {'symbol': 'TITAN.NS', 'description': 'Titan Company'},
    {'symbol': 'ULTRACEMCO.NS', 'description': 'UltraTech Cement'},
    {'symbol': 'POWERGRID.NS', 'description': 'Power Grid Corporation'},
    {'symbol': 'TECHM.NS', 'description': 'Tech Mahindra'},
    {'symbol': 'CIPLA.NS', 'description': 'Cipla Ltd'},
    {'symbol': 'DRREDDY.NS', 'description': 'Dr Reddys Laboratories'},
    {'symbol': 'EICHERMOT.NS', 'description': 'Eicher Motors Royal Enfield'},
    {'symbol': 'HEROMOTOCO.NS', 'description': 'Hero MotoCorp'},
    {'symbol': 'BPCL.NS', 'description': 'Bharat Petroleum'},
    {'symbol': 'IOC.NS', 'description': 'Indian Oil Corporation'},
    {'symbol': 'COALINDIA.NS', 'description': 'Coal India'},
    {'symbol': 'JSWSTEEL.NS', 'description': 'JSW Steel'},
    {'symbol': 'HINDALCO.NS', 'description': 'Hindalco Industries'},
    {'symbol': 'INDUSINDBK.NS', 'description': 'IndusInd Bank'},
    {'symbol': 'BANDHANBNK.NS', 'description': 'Bandhan Bank'},
    {'symbol': 'PNB.NS', 'description': 'Punjab National Bank'},
    {'symbol': 'BANKBARODA.NS', 'description': 'Bank of Baroda'},
    {'symbol': 'GRASIM.NS', 'description': 'Grasim Industries'},
    {'symbol': 'ADANIPORTS.NS', 'description': 'Adani Ports'},
    {'symbol': 'ADANIGREEN.NS', 'description': 'Adani Green Energy'},
    {'symbol': 'ADANIPOWER.NS', 'description': 'Adani Power'},
    {'symbol': 'MUTHOOTFIN.NS', 'description': 'Muthoot Finance'},
    {'symbol': 'PIDILITIND.NS', 'description': 'Pidilite Industries Fevicol'},
    {'symbol': 'HAVELLS.NS', 'description': 'Havells India'},
    {'symbol': 'VOLTAS.NS', 'description': 'Voltas Ltd'},
    {'symbol': 'GODREJCP.NS', 'description': 'Godrej Consumer Products'},
    {'symbol': 'MARICO.NS', 'description': 'Marico Ltd'},
    {'symbol': 'DABUR.NS', 'description': 'Dabur India'},
    {'symbol': 'COLPAL.NS', 'description': 'Colgate Palmolive India'},
    {'symbol': 'TITAN.NS', 'description': 'Titan Company'},
    {'symbol': 'TRENT.NS', 'description': 'Trent Zudio Westside'},
    {'symbol': 'NAUKRI.NS', 'description': 'Info Edge Naukri'},
    {'symbol': 'POLICYBZR.NS', 'description': 'PB Fintech PolicyBazaar'},
    {'symbol': 'DELHIVERY.NS', 'description': 'Delhivery Ltd'},
    {'symbol': 'RVNL.NS', 'description': 'Rail Vikas Nigam RVNL'},
    {'symbol': 'IRFC.NS', 'description': 'Indian Railway Finance IRFC'},
    {'symbol': 'HAL.NS', 'description': 'Hindustan Aeronautics HAL'},
    {'symbol': 'BEL.NS', 'description': 'Bharat Electronics BEL'},
    {'symbol': 'NHPC.NS', 'description': 'NHPC Ltd'},
    {'symbol': 'SJVN.NS', 'description': 'SJVN Ltd'},
]

_price_cache = {}

def get_quote(symbol: str):
    sym = symbol.upper()
    try:
        ticker = yf.Ticker(sym)
        info = ticker.fast_info
        price = info.last_price
        prev = info.previous_close
        if price and price > 0:
            _price_cache[sym] = round(price, 2)
            return {'c': round(price, 2), 'pc': round(prev, 2) if prev else price, 'symbol': sym}
        # fallback to history if fast_info fails
        hist = ticker.history(period='1d', interval='1m')
        if not hist.empty:
            price = round(float(hist['Close'].iloc[-1]), 2)
            _price_cache[sym] = price
            return {'c': price, 'pc': price, 'symbol': sym}
        # last resort: use cached price
        if sym in _price_cache:
            return {'c': _price_cache[sym], 'pc': _price_cache[sym], 'symbol': sym}
        return None
    except Exception:
        if sym in _price_cache:
            return {'c': _price_cache[sym], 'pc': _price_cache[sym], 'symbol': sym}
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
