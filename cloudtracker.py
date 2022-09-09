from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from datetime import datetime, timezone
from dateutil import tz
client = Client(key="api_key",
                'api_secret') # Enter your own API details from binance here


def calculateKijun(highs, lows, delay):
    """
    Calculates (26 period high + 26 period low) / 2
    Also known as the "Kijun-sen" line
    """
    try:

        high_prices = highs[(-61-delay):(-1-delay)]
        low_prices = lows[(-61-delay):(-1-delay)]
        period_high = float(max(high_prices))
        period_low = float(min(low_prices))
        kijun = ((period_high + period_low) / 2)
        return (kijun)
    except Exception as e:
        ebt = True

def calculateTenkan(highs, lows, delay):
    """
    Calculates (9 period high + 9 period low) / 2
    Also known as the "Tenkan-sen" line
    """
    try:

        high_prices = highs[(-21-delay):(-1-delay)]
        low_prices = lows[(-21-delay):(-1-delay)]
        period_high = float(max(high_prices))
        period_low = float(min(low_prices))
        tenkan = ((period_high + period_low) / 2)
        return (tenkan)
    except Exception as e:
        ebt = True

def calculateBottomCloud(highs, lows, delay):
    """
    Calculates (120 period high + 120 period low) / 2
    Also known as the "Bottom cloud" line
    """
    try:

        high_prices = highs[(-121-delay):(-1-delay)]
        low_prices = lows[(-121-delay):(-1-delay)]
        period_high = float(max(high_prices))
        period_low = float(min(low_prices))
        bottomCloud = ((period_high + period_low) / 2)
        #print('bottom cloud:',bottomCloud)
        return (bottomCloud)
    except Exception as e:
        ebt = True
def calculateTopCloud(highs, lows, delay):
    """top cloud = kijun + tenkan / 2
    """
    kijun = calculateKijun(highs,lows,delay)
    tenkan = calculateTenkan(highs,lows,delay)
    return ((kijun + tenkan) / 2)
def analyzeCloud(market,timeframe):
    goSignals = []
    if timeframe is "week":
        agostring = "200 week ago"
        timeframe = Client.KLINE_INTERVAL_1WEEK
    elif timeframe is "day":
        agostring = "200 day ago"
        timeframe = Client.KLINE_INTERVAL_1DAY
    candles = client.get_historical_klines(market,timeframe,agostring)
    highs = []
    lows = []
    price = []

    for i in range(len(candles)):
        highs.append(candles[i][2])
        lows.append(candles[i][3])
        price.append(candles[i][4])
    kl = calculateKijun(highs,lows,0) # Kijun line
    okl = calculateKijun(highs,lows,1) # 1 period old Kijun line
    tl = calculateTenkan(highs,lows,0) # Tenkan line
    otl = calculateTenkan(highs,lows,1) # 1 period old tenkan line
    tc = calculateTopCloud(highs,lows,30) # A line of cloud in line with price
    bc = calculateBottomCloud(highs,lows,30) # b line of cloud in line with price // A line > b line == Green cloud
    lbc = calculateBottomCloud(highs,lows,58) # b line of cloud 30 days ago, for lagging span price
    ltc = calculateTopCloud(highs,lows, 58) # A line of cloud 30 days ago for lagging span price
    ftc = calculateTopCloud(highs,lows,0) # Cloud 30 periods into future (for checking for kumo twist)
    fbc = calculateBottomCloud(highs,lows,0) # b line 30 periods into future
    otc = calculateTopCloud(highs,lows,1)
    obc = calculateBottomCloud(highs,lows,1) # clouds delayed by 1 day
    cp = float(price[-1])
    #print(otc,obc,ftc,fbc)

    if (tl > kl) and (otl < okl):
        goSignals.append("FRESH TK CROSS")
        print(market," Has a fresh TK Cross")
    if (tl*.995 <= kl <= tl*1.005) and (otl < okl):
        goSignals.append("NEARING TK CROSS")
        print(market, " Nearing TK Cross")
    if (tc > bc) and (ftc > fbc):
        goSignals.append("Green cloud")
    if (0.995 <= (ftc/fbc) <= 1.005) and (obc > otc):
        goSignals.append("Possible Kumo twist")
    if (cp > ltc) and (cp > lbc):
        goSignals.append("Lagging span above cloud")
    if (cp > tc) and (cp > bc):
        goSignals.append("Price above cloud")
    if len(goSignals) >= 4:
        print(market," has", len(goSignals), " Bullish signals on the cloud.\n")
        for i in range(len(goSignals)):
            print(goSignals[i],"\n")


# Get all tickers and narrow them to USD pairs

info = client.get_all_tickers()
search_key = 'USD'
USD_pairs = []
timeframe = "day" #'week' or 'day'

for i in range(len(info)):
    if 'USD' in info[i]['symbol']:
        USD_pairs.append(info[i]['symbol'])

for i in range(len(USD_pairs)):
    try:
        analyzeCloud(USD_pairs[i],timeframe)
    except Exception as e:
        x = True #Dummy except to just skip errors
