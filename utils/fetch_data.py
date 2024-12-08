import requests
# from config import API_KEY

# API_KEY = '79602108dd4545a1953b792daa73b248bbf9b14a'
API_KEY = '9a19db152424baf1aa1e20de497d038a0997ba45'

def fetch_data(stock_symbol, start_date, end_date):
    """
    Fetches stock price data for the specified symbol and date range.
    """
    print("Fetching data from Tiingo API...")
    url = f"https://api.tiingo.com/tiingo/daily/{stock_symbol}/prices?startDate={start_date}&endDate={end_date}"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Token {API_KEY}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.json()}")

    data = response.json()
    return [
        {"timestamp": item["date"], "open": item["open"], "close": item["close"], "high": item["high"], "low": item["low"], "volume": item["volume"]}
        for item in data if item["close"] is not None
    ]
