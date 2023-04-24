import backtrader 
import datetime
from strategies import TestStrategy

# example from https://www.youtube.com/watch?v=K8buXUxEfMc&list=PLpf4_DgAsgLFWuT2uV3NItcV4elJUc78J&index=3

cerebro = backtrader.Cerebro() # initiate cerebro object

cerebro.broker.set_cash(1000000) # gave broker attribute an initial value of 1 million

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Create a Data Feed
data = backtrader.feeds.YahooFinanceCSVData(
    dataname='oracle.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2000, 12, 31),
    reverse=False)

# Connect the Data Feed to Cerebro
cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())