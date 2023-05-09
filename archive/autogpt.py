# Import the backtrader platform
import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf

# Define the strategy class
class DualThrust(bt.Strategy):
    params = (
        ('lookback', 20),
        ('atr_multiplier', 2.0),
        ('stop_loss_pct', 0.05),
        ('trailing_stop_pct', 0.05),
        ('risk_per_trade_pct', 0.02),
        ('max_drawdown_pct', 0.1),
        ('data_source', 'yahoo'),
        ('optimization_method', 'grid_search'),
        ('position_sizing_method', 'fixed'),
        ('position_sizing_factor', 0.1),
        ('logging', True),
        ('error_handling', True),
        ('strategy_analyzer', True),
        ('machine_learning', False),
        ('cloud_platform', False)
    )

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(period=self.params.lookback)
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Commission: {order.executed.comm}")

            elif order.issell():
                self.log(f"SELL EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Commission: {order.executed.comm}")

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data.close[0] > self.data.open[0] + self.atr[0] * self.params.atr_multiplier:
                self.order = self.buy()
        else:
            if self.data.close[0] < self.data.open[0] - self.atr[0] * self.params.atr_multiplier:
                self.order = self.sell()

# Download data using yfinance
data = yf.download("AAPL", start="2020-01-01", end="2022-12-31")

# Create a Backtrader data feed
data_feed = btfeeds.PandasData(dataname=data)

# Initialize the Backtrader engine
cerebro = bt.Cerebro()

# Add the data feed to the engine
cerebro.adddata(data_feed)

# Add the strategy to the engine
cerebro.addstrategy(DualThrust)

# Set the starting cash for the engine
cerebro.broker.setcash(10000.0)

# Set the commission for the engine
cerebro.broker.setcommission(commission=0.001)

# Run the engine
cerebro.run()

# Print the final portfolio value
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

# Plot the results
cerebro.plot()
