
import streamlit as st
import backtrader as bt
import yfinance as yf

class MACDStrategy(bt.Strategy):
    params = (
        ("macd1", 12),
        ("macd2", 26),
        ("macdsig", 9),
        ("stop_loss", 0.03),
        ("take_profit", 0.05),
        ("trail_stop", True),
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.macdsig,
        )

    def next(self):
        if not self.position:
            if self.macd.macd[0] > self.macd.signal[0]:
                size = self.broker.getcash() / self.data.close[0]
                self.buy(size=size)
        elif self.macd.macd[0] < self.macd.signal[0]:
            self.close()

def run_backtest(strategy):
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=yf.download("TSLA", start="2010-01-01", end="2022-12-31"))
    cerebro.adddata(data)

    cerebro.addstrategy(strategy)
    cerebro.broker.set_cash(1000)
    cerebro.broker.setcommission(commission=0.001)

    st.write("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    st.write("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    return cerebro



st.title("Backtrader Backtesting App")

st.write("This app runs a backtest on the MACDStrategy using historical price data from the yfinance library.")
run_button = st.button("Run Backtest")

if run_button:
    cerebro = run_backtest(MACDStrategy)
    st.write("Backtest completed. Check the results above.")

    st.write("Plotting the backtest results...")
    import io
    import base64
    from PIL import Image

    img = io.BytesIO()
    cerebro.plot(style='candlestick', savefig=True, dpi=100, tight_layout=True, figfilename=img)
    img.seek(0)
    st.image(img, caption="Backtest Results", use_column_width=True)

# I believe this one worked on backtrader which is great 
