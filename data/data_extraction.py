import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
from utils.fetch_data import fetch_data
from termcolor import colored

# Adjusted today for simulation purposes
# adjusted_today = datetime.now() 
adjusted_today = datetime.now() - timedelta(days=5)


def filter_last_five_days(data):
    """
    Filters the last 5 trading days from the data.
    :param data: List of trading data.
    :return: Filtered data for the last 5 trading days.
    """
    # Use the last 5 elements as they represent the last trading days
    return data[-5:]


def generate_buy_sell_signals(data):
    """
    Generates buy/sell/hold signals based on closing prices.
    """
    signals = []
    for i in range(1, len(data)):
        signal = "HOLD"
        if data[i]['close'] > data[i - 1]['close']:
            signal = "BUY"
        elif data[i]['close'] < data[i - 1]['close']:
            signal = "SELL"

        signals.append({
            "timestamp": data[i]['timestamp'],
            "close": data[i]['close'],
            "signal": signal
        })

    return signals


def most_frequent_signal(signals):
    """
    Predicts the trend based on the most frequent signal.
    """
    signal_counts = Counter(signal['signal'] for signal in signals)
    most_common_signal, count = signal_counts.most_common(1)[0]
    return most_common_signal


def analyze_data(stock_symbol):
    """
    Fetches two months of data, determines last 5 trading days, and analyzes today's trend.
    """
    # Date range for two months
    start_date = (adjusted_today - pd.Timedelta(days=55)).strftime('%Y-%m-%d')
    end_date = datetime.now()
    # print("From data_extraction.py: start_date: ", start_date, " end_date: ", end_date)
    # Fetch data via fetch_data.py
    data = fetch_data(stock_symbol, start_date, end_date)

    # dataSend send should be 5 days less than the current date
    # dont call the api again, use the data fetched above start to end -5
    dataSend = data[:-4]
    # adjusted_today = last 5th from data fetched

    # print("adjusted today: ", data[-5]['timestamp'])
    adjusted_today_new = datetime.strptime(data[-5]['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")    # Filter last 5 days
    last_five_days_data = filter_last_five_days(data)
    
    # Ensure trade date is today - 5
    trade_date = adjusted_today_new.strftime('%Y-%m-%d')

    # Analyze signals
    signals = generate_buy_sell_signals(last_five_days_data)
    most_common_signal = most_frequent_signal(signals)

    # Print results
    print(colored(f"The trend for {trade_date} is: {most_common_signal}", 'cyan'))
    print(colored(f"Trade price: {last_five_days_data[-5]['close']} (Close)", 'green'))
    print(colored("Prices for the last 5 trading days:", 'yellow'))
    for day in last_five_days_data:
        print(colored(f"Date: {day['timestamp']}, Open: {day['open']}, Close: {day['close']}, Volume: {day['volume']}", 'magenta'))

    return dataSend, trade_date, last_five_days_data[-5]['close'], last_five_days_data


if __name__ == "__main__":
    # Analyze data for Google stock
    analyze_data(stock_symbol="GOOGL")
