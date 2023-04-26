import backtrader as bt

class PrintClose(bt.Strategy):

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') # Print date and close

    def next(self):
        self.log('Close: ' + str(self.dataclose[0]))  # Convert the float to a string

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add data feed to Cerebro
data = bt.feeds.YahooFinanceCSVData(dataname='TSLA.csv', datetime=0)
cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(PrintClose)

# Run Cerebro Engine
cerebro.run()
