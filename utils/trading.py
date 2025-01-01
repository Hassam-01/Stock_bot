
from datetime import datetime, timedelta
import requests

def make_trade(signal, price_per_stock):
    """
    
    arguments:
        symbol (str): The stock symbol to trade.
        action (str): The action to perform ('buy' or 'sell').
        quantity (int): The number of stocks to trade.

    Returns:
        dict: A dictionary containing trade details.
    """
    # Log the trade
    trade_details = {
        "signal": signal,
        "price_per_stock": price_per_stock,
        "trade_time": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"),
        }

    # Print the trade details33[
    print("\033[92mTrade Executed:\033[0m")
    print(f"Signal: \033[91m{trade_details['signal']}\033[0m")
    print(f"\033[92mPrice per stock: ${trade_details['price_per_stock']}\033[0m")
    print(f"\033[92mTrade Time: {trade_details['trade_time']}\00m")
    print("\033[91m---------------------------------------------------------------\033[0m")  

    return trade_details

