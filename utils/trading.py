
import random
from datetime import datetime
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


def make_trade(symbol, action, quantity):
    """
    Simulate a local trade without calling any API.
    
    Args:
        symbol (str): The stock symbol to trade.
        action (str): The action to perform ('buy' or 'sell').
        quantity (int): The number of stocks to trade.

    Returns:
        dict: A dictionary containing trade details.
    """
    # Simulate a stock price for the trade
    price_per_stock = round(random.uniform(50, 5000), 2)  # Random price between $50 and $5000
    total_price = round(price_per_stock * quantity, 2)

    # Log the trade
    trade_details = {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "price_per_stock": price_per_stock,
        "total_price": total_price,
        "trade_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Print the trade details
    print("Trade Executed:")
    print(f"Symbol: {trade_details['symbol']}")
    print(f"Action: {trade_details['action']}")
    print(f"Quantity: {trade_details['quantity']}")
    print(f"Price per stock: ${trade_details['price_per_stock']}")
    print(f"Total price: ${trade_details['total_price']}")
    print(f"Trade Time: {trade_details['trade_time']}")

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
