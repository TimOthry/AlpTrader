from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, MarketOrderRequest
from alpaca.trading.enums import AssetClass, OrderSide, TimeInForce
from dotenv import load_dotenv
import os

load_dotenv()
trading_client = TradingClient(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), paper=True)

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Search for all US stocks available
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
assets = trading_client.get_all_assets(search_params)
for asset in assets:
    if asset.tradable:
        print("Symbol: " + asset.symbol + " Name: " + asset.name)
