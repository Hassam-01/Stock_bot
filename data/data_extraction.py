import requests
import pandas as pd
from datetime import datetime
from collections import Counter


API_KEY = "79602108dd4545a1953b792daa73b248bbf9b14a"

def last_five_days(symbol,API_KEY="79602108dd4545a1953b792daa73b248bbf9b14a"):
    """To infer today's trend, checking the last five days"""

    start_date = (datetime.now() - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={start_date}&endDate={end_date}"
    # Headers with the API key for authentication
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {API_KEY}',  # Ensure the key is passed correctly here
    }

    # Send the request to the Tiingo API
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.json()}")

    data = response.json()

    return [
        {"timestamp": item["date"], "open": item["open"], "close": item["close"]}
        for item in data if item["close"] is not None
    ]


def generate_buy_sell_signals(data):
    """
        Generating a signal
        (BUY,SELL or HOLD)
    """
    signals = []

    # Generate buy/sell signals based on closing prices
    for i in range(1, len(data)):
        signal = ""
        # Price is increasing
        if data[i]['close'] > data[i - 1]['close']:
            signal = "BUY"
        # Price is decreasing
        elif data[i]['close'] < data[i - 1]['close']:
            signal = "SELL"
        else:
            # No change in price
            signal = "HOLD"

        signals.append({
            "timestamp": data[i]['timestamp'],
            "close": data[i]['close'],
            "signal": signal
        })

    return signals


def most_frequent_signal(signals):
    """Predicting the trend from the most frequent"""
    # Use Counter to count the occurrences of each signal
    signal_counts = Counter(signal['signal'] for signal in signals)
    most_common_signal, count = signal_counts.most_common(1)[0]

    return most_common_signal

def data_two_months(symbol,API_KEY="79602108dd4545a1953b792daa73b248bbf9b14a"):
    """

    :param symbol: Symbol of the company e.g APPL
    :return: data dictionary
    """
    #dates for data extraction
    start_date = (datetime.now() - pd.Timedelta(days=55)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={start_date}&endDate={end_date}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {API_KEY}',  # Ensure the key is passed correctly here
    }

    # Send the request to the Tiingo API
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.json()}")

    data = response.json()
    return [
        {"timestamp": item["date"], "open": item["open"], "close": item["close"]}
        for item in data if item["close"] is not None
    ]

def fetch_data_for_today(symbol):
    """main for the today's trend function"""
    stock_data = last_five_days(symbol)
    if stock_data:
        signals = generate_buy_sell_signals(stock_data)
        # Find the most frequent signal
        most_common_signal= most_frequent_signal(signals)
        print(f"The trend of today is: {most_common_signal}")

if __name__ == "__main__":
    data = data_two_months(symbol="GOOGL")
    print(data)
