from Stock import Stock


def main():
    tickers = ["MSFT", "TSLA", "FB", "GOOG", "AAPL", "P"]  # add whichever stock ticker you would like to check
    stocks = []  # stock objects as created in the Stock class

    for i in tickers:
        stocks.append(Stock(i))

    # prints info on each stock to the console
    for i in range(len(stocks)):
        print(stocks[i].getTicker())
        print("Initial Investment: $", stocks[i].startingInvestment, sep="")
        print("Day 1 Open: $", stocks[i].openingPrices[0], sep="")
        print("Final Day Close: $", stocks[i].closingPrices[-1], sep="")
        print("MVA Return: $", stocks[i].getReturnMVA(), sep="")
        print("MVA Return Percentage: ", stocks[i].getPercentReturnMVA(), "%", sep="")
        print("Current Cash: $", stocks[i].getCurrentCash(), sep="")
        print()


main()
