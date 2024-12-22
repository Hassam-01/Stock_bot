
from datetime import datetime, timedelta
import requests

# Example API URL (replace with actual API endpoint)
API_URL = 'https://api.stockdata.com/v1/stock_data'  # Replace with the correct API URL

def fetch_data_from_api():
    """
    Function to fetch stock data from an external API.
    This function assumes the API provides stock data in JSON format.
    """
    try:
        # Make the GET request to the API
        response = requests.get(API_URL)
        # Raise an exception if the request was not successful
        response.raise_for_status()
        # Return the JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any exception that occurs during the request
        print(f"Error fetching data from API: {e}")
        return None


def make_trade(signal, price_per_stock):
    """
    Simulate a local trade without calling any API.
    
    Args:
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



if __name__ == '__main__':
    # Example usage
    data = fetch_data_from_api()
    if data:
        print("Fetched Stock Data:", data)

    # Example trade (buy 10 shares of AAPL)
    trade_response = make_trade('AAPL', 'buy', 10)
    if trade_response:
        print("Trade Execution Status:", trade_response)
