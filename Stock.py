import urllib.request
import json


class Stock:
    def __init__(self, ticker):
        self.key = "&apikey=ONLW79KFJ50YBIRZ"  # API key for AlphaVantage
        data = self.getData(ticker, self.key)

        self.startingInvestment = 1000  # starting investment in dollars (default $1000)
        self.currentMoney = self.startingInvestment
        self.shares = 0  # number of shares currently owned in a given stock (default 0)
        self.ticker = data['Meta Data']['2. Symbol']
        self.prices = data['Time Series (Daily)']

        # stores all daily opening prices in list
        self.openingPrices = []
        for key in data['Time Series (Daily)']:
            self.openingPrices.append(float(data['Time Series (Daily)'][key]['1. open']))

        # all daily highs
        self.highs = []
        for key in data['Time Series (Daily)']:
            self.highs.append(float(data['Time Series (Daily)'][key]['2. high']))

        # all daily lows
        self.lows = []
        for key in data['Time Series (Daily)']:
            self.highs.append(float(data['Time Series (Daily)'][key]['3. low']))

        # all daily closing prices
        self.closingPrices = []
        for key in data['Time Series (Daily)']:
            self.closingPrices.append(float(data['Time Series (Daily)'][key]['4. close']))

        # moving 5 day average
        self.mva = self.calcMVA()

        # calculates the total return amount by calling buy low and sell high functions
        # according to closing prices and MVA. Sells all shares on day 95
        for i in range(95):
            if self.mva[i] < self.closingPrices[i + 5] and self.shares == 0 and i != 94:
                self.buyLow(i)
            elif self.mva[i] > self.closingPrices[i + 5] and self.shares != 0 or i == 94:
                self.sellHigh(i)

    # decodes the stock data from AlphaVantage given a ticker
    def getData(self, ticker, key):
        with urllib.request.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
                                    + ticker + key) as url:
            stock = json.loads(url.read().decode())
            return stock

    # method to set an api key different from the default
    def setAPI(self, api):
        self.key = api

    # allows user to select their own investment amount
    def setStartingInvestment(self, amount):
        self.startingInvestment = amount

    # get methods for data
    def getTicker(self): return self.ticker

    def getOpen(self): return self.openingPrices

    def getHigh(self): return self.highs

    def getLow(self): return self.lows

    def getClose(self): return self.closingPrices

    def getCurrentCash(self): return round(self.currentMoney, 2)

    def calcMVA(self):  # moving 5 day average
        mva = []
        for num in range(len(self.highs) - 5):
            avg = sum(self.highs[num: num + 5]) / 5
            mva.append(avg)
        return mva

    def getMVA(self): return self.mva

    # invests all of initial investment plus any dividends
    def buyLow(self, i):
        self.shares = self.currentMoney // self.highs[i]
        self.currentMoney -= (self.highs[i] * self.shares)

    # sells all shares owned in the specified stock
    def sellHigh(self, i):
        self.currentMoney += (self.highs[i] * self.shares)
        self.shares = 0

    # total return using the moving average method for trading
    def getReturnMVA(self):
        return round(self.currentMoney - self.startingInvestment, 2)

    # percent return using moving average method
    def getPercentReturnMVA(self):
        return round(((self.currentMoney - self.startingInvestment) / self.startingInvestment) * 100, 2)
