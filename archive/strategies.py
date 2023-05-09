import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.LOG('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)
            
        self.order=None # reset the order attribute to None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # print(len(self))
        # print(self.order)
        # print(self.position)

        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]: # checking the index (0 is current, -1 is previous). so we are 
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]: # this would indicate a slight dip in the price and trigger a buy. it is saying 
                                                            # if the previous close is less than the one before it, then buy                  
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0]) # log the buy price. self.dataclose[0] is the current price that we are buying at
                    self.order = self.buy()
        else: 
            if len(self)>=(self.bar_executed +5):
                self.log('SELL CREATED {}'.format(self.dataclsoe[0]))
                self.order = self.sell() 