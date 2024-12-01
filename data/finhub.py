import requests
from collections import Counter
import json

# Alpha Vantage API key
API_KEY = " IQT5ULOHVG0MASPA"

# Stock symbol (e.g., AAPL for Apple)
symbol = 'MSFT'

def fetch_data_for_today(symbol,API_KEY):
    # API URL
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact'

    # Get data from Alpha Vantage
    response = requests.get(url)
    data = response.json()


    # Extract the time series data
    time_series = data.get('Time Series (Daily)', {})
    data = time_series

    # Get the last 5 days (ensure there are at least 5 days of data)
    last_5_days = {date: time_series[date] for date in list(time_series.keys())[:5]}

    suggested_action = []
    # Print the last 5 days' data
    for date, stats in last_5_days.items():
        print(f"Date: {date}")
        print(f"Open: {stats['1. open']}")
        print(f"High: {stats['2. high']}")
        print(f"Low: {stats['3. low']}")
        print(f"Close: {stats['4. close']}")
        print(f"Volume: {stats['5. volume']}")
        print("--------")



        # Extract the last 5 closing prices
        closing_prices = [data[date]['4. close'] for date in data]

        for i in range(len(closing_prices)):
            closing_prices[i] = float(closing_prices[i])

        # Calculate the Simple Moving Average (SMA) for the last 5 days
        sma = sum(closing_prices) / len(closing_prices)

        # Get today's close price (last in the list)
        today_close = closing_prices[-1]
        yesterday_close = closing_prices[-2]

        # Determine trend based on close prices
        if today_close > yesterday_close:
            trend = 'Buy'  # Upward trend (Bullish)
        elif today_close < yesterday_close:
            trend = 'Sell'  # Downward trend (Bearish)
        else:
            trend = 'Hold'  # Neutral trend

        suggested_action.append(trend)

        # Print the results
        print(f"Today's Close: {today_close}")
        print(f"Yesterday's Close: {yesterday_close}")
        print(f"SMA (5 days): {sma}")
        print(f"Suggested Action: {trend}")

    count = Counter(suggested_action)

    # Find the string with the maximum occurrence
    max_occurrence = count.most_common(1)
    trend_of_the_day = max_occurrence[0][0]
    print(f"The trend for the today is {trend_of_the_day}")
fetch_data_for_today(symbol,API_KEY)