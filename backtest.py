from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

# Mean Reversion Strategy Backtest
class MeanReversion(Strategy):

    moving_average_window = 20
    threshold = 2

    def initialize(self):
        self.ma = self.I(self.data.Close.rolling, self.moving_average_window).mean()
        self.std = self.I(self.data.Close.rolling, self.moving_average_window).std()
    
    def on_trading_iteration(self):
        # Get the current price of the asset
        current_price = self.get_last_price("AAPL")
        moving_avg = self.ma[-1]
        moving_std = self.std[-1]

        # Calculate the upper and lower bands
        upper_band = moving_avg + self.threshold * moving_std
        lower_band = moving_avg - self.threshold * moving_std

        # Trading logic
        if current_price < lower_band:
            # Check if we are not already in a position before buying
            if not self.is_position_open("AAPL"):
                self.buy("AAPL")
        elif current_price > upper_band:
            # Check if we are in a position before selling
            if self.is_position_open("AAPL"):
                self.sell("AAPL")

    def is_position_open(self, symbol):
        # Check if the position for the given symbol is open
        return symbol in self.positions

backtest_start = datetime(2022, 1, 1)
backtest_end = datetime(2022, 12, 31)

MeanReversion.backtest(
    YahooDataBacktesting,
    backtest_start,
    backtest_end,
)