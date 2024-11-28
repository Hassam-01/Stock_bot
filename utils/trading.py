# tradingBot.py
import requests
from plotData import plot_data  # Importing the plot function from plotData.py

# Example function to fetch data from API (you can replace this with your actual API call)
def fetch_data_from_api():
    # Example API endpoint (replace with your actual API endpoint)
    url = 'https://api.example.com/stock_data'
    response = requests.get(url)

    if response.status_code == 200:
        # Assuming the API returns data in JSON format with 'timestamps', 'open', 'close', 'predictions'
        data = response.json()
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Fetch the data from the API
data = fetch_data_from_api()

if data:
    timestamps = data['timestamps']  # Example data field
    open_prices = data['open']        # Example data field
    close_prices = data['close']      # Example data field
    predictions = data.get('predictions', None)  # Optional, might not always be present

    # Now call the plot function from plotData.py to plot the data
    plot_data(timestamps, open_prices, close_prices, predictions)
