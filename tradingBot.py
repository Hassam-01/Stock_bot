import numpy as np
import requests
from scipy.stats import linregress
import random
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from utils.plotData import plotData

# ! IGNORE THIS FILE

# Tiingo API Configuration
API_KEY = '9a19db152424baf1aa1e20de497d038a0997ba45'  # Replace with your Tiingo API key

# List of valid stock symbols
VALID_STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'FB', 'NVDA', 'AMD', 'SPY']

# Initialize portfolio
portfolio = {
    "cash": 10000,  # Starting cash
    "stock": 0,     # Number of shares
    "last_buy_price": 0  # Price at the last buy
}

# Adjusted thresholds for genetic algorithm
GENE_POOL = [0.2, 0.3, 0.4, -0.2, -0.3, -0.4]
BEST_GENES = {'BUY_THRESHOLD': 0.3, 'SELL_THRESHOLD': -0.3}

# Markov Transition Matrix
MARKOV_MATRIX = {
    'UP': {'UP': 0.6, 'DOWN': 0.3, 'STABLE': 0.1},
    'DOWN': {'UP': 0.2, 'DOWN': 0.5, 'STABLE': 0.3},
    'STABLE': {'UP': 0.3, 'DOWN': 0.3, 'STABLE': 0.4}
}

# Visualization Data
trend_data = {
    "timestamps": [],
    "open_prices": [],
    "close_prices": [],
    "predictions": []
}


# Prompt user for stock symbol and time range
def get_user_input():
    """
    Prompts the user to select a stock and a time range.
    """
    print("Please select a stock from the following list:")
    for i, stock in enumerate(VALID_STOCKS, 1):
        print(f"{i}. {stock}")
    stock_choice = int(input("Enter the number of the stock you want to trade: ")) - 1
    stock_symbol = VALID_STOCKS[stock_choice]
    
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    return stock_symbol, start_date, end_date

def predict_missing_values(prices):
    """
    Predicts missing values using linear regression.
    """
    if len(prices) < 2:  # Not enough data points to predict
        return prices

    # Prepare data for prediction
    valid_prices = [(i, price) for i, price in enumerate(prices) if price is not None]
    
    if len(valid_prices) < 2:  # If less than two valid points, skip prediction
        return prices
    
    # Separate data into x and y for linear regression
    x = np.array([i for i, _ in valid_prices]).reshape(-1, 1)
    y = np.array([price for _, price in valid_prices])

    # Fit linear regression model
    model = LinearRegression().fit(x, y)

    # Predict missing values
    for i in range(len(prices)):
        if prices[i] is None:
            prices[i] = model.predict([[i]])[0]

    return prices

def calculate_slope(prices):
    """
    Calculates the slope of the price trend using linear regression.
    Handles cases where data might be insufficient.
    """
    if len(prices) < 2:  # Not enough data points to calculate slope
        return float('nan')  # Indicate that the slope is not computable
    x = np.arange(len(prices))
    try:
        slope, _, _, _, _ = linregress(x, prices)
        return slope
    except ValueError:  # Handle the case where `linregress` fails (e.g., all data points are the same)
        return float('nan')

def calculate_volatility(prices):
    """
    Calculates volatility as the standard deviation of price changes.
    Handles cases where data might be insufficient.
    """
    if len(prices) < 2:  # Not enough data points to calculate volatility
        return float('nan')  # Indicate that volatility is not computable
    return np.std(np.diff(prices))

def markov_prediction(current_state):
    """
    Predicts the next state using Markov transition probabilities.
    """
    probabilities = MARKOV_MATRIX[current_state]
    next_state = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    return next_state

def genetic_algorithm(prices):
    """
    Optimizes buy/sell thresholds using a genetic algorithm.
    """
    global BEST_GENES
    population = [{'BUY_THRESHOLD': random.choice(GENE_POOL), 'SELL_THRESHOLD': random.choice(GENE_POOL)} for _ in range(10)]
    
    def fitness(genes):
        slope = calculate_slope(prices)
        return abs(genes['BUY_THRESHOLD'] - slope) + abs(genes['SELL_THRESHOLD'] + slope)
    
    population = sorted(population, key=fitness)
    BEST_GENES = population[0]

def apply_fuzzy_logic(slope, volatility, next_state):
    """
    Applies fuzzy logic combined with Markov prediction to generate trading signals.
    Adjusted to increase chances of trade execution.
    """
    if next_state == 'UP' and slope > 0.1 and volatility < 0.05:  # Looser buy condition
        return 'BUY'
    elif next_state == 'DOWN' and slope < -0.1 and volatility > 0.05:  # Looser sell condition
        return 'SELL'
    else:
        return 'HOLD'

def make_trade(signal, current_price):
    """
    Executes a trade based on the signal.
    Includes a log for trade execution success/failure.
    """
    global portfolio
    if signal == 'BUY' and portfolio['cash'] >= current_price:
        num_shares = int(portfolio['cash'] // current_price)
        if num_shares > 0:
            portfolio['cash'] -= num_shares * current_price
            portfolio['stock'] += num_shares
            portfolio['last_buy_price'] = current_price
            print(f"Bought {num_shares} shares at ${current_price:.2f}")
    elif signal == 'SELL' and portfolio['stock'] > 0:
        portfolio['cash'] += portfolio['stock'] * current_price
        print(f"Sold {portfolio['stock']} shares at ${current_price:.2f}")
        portfolio['stock'] = 0
    else:
        print(f"No trade executed. Signal: {signal}, Cash: {portfolio['cash']:.2f}, Stock: {portfolio['stock']}")


def fetch_data(stock_symbol, start_date, end_date):
    """
    Fetches historical stock data from Tiingo's API.
    """
    url = f"https://api.tiingo.com/tiingo/daily/{stock_symbol}/prices?startDate={start_date}&endDate={end_date}"  
    headers = {'Content-Type': 'application/json', 'Authorization': f'Token {API_KEY}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.json()}")
    
    data = response.json()
    
    # Print the entire fetched data for debugging
    print("Fetched Data from Tiingo API:")
    # print(data)
    plotData(data)
    # Filter out None or invalid data points
    stock_data = [{"timestamp": item["date"], "open": item["open"], "close": item["close"]} for item in data if item["close"] is not None]
    return stock_data


def start_trading_loop():
    stock_symbol, start_date, end_date = get_user_input()
    
    current_state = 'STABLE'
    while True:
        try:
            # Fetch and process data
            stock_data = fetch_data(stock_symbol, start_date, end_date)
            timestamps = [datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ") for item in stock_data]
            open_prices = [item["open"] for item in stock_data]
            close_prices = [item["close"] for item in stock_data]
            
            # Store data for plotting
            trend_data["timestamps"] = timestamps
            trend_data["open_prices"] = open_prices
            trend_data["close_prices"] = close_prices
            
            # Calculate indicators
            slope = calculate_slope(close_prices)
            volatility = calculate_volatility(close_prices)
            
            # Skip iteration if indicators are invalid
            if np.isnan(slope) or np.isnan(volatility):
                print(f"Invalid data: Slope={slope}, Volatility={volatility}. Retrying...")
                time.sleep(60)
                continue
            
            # Optimize thresholds and make predictions
            genetic_algorithm(close_prices)
            next_state = markov_prediction(current_state)
            trend_data["predictions"].append(next_state)
            current_state = next_state
            
            # Generate trading signal
            signal = apply_fuzzy_logic(slope, volatility, next_state)
            print(f"Slope: {slope:.4f}, Volatility: {volatility:.4f}, Next State: {next_state}, Signal: {signal}")
            
            # Execute trade
            current_price = close_prices[-1]
            make_trade(signal, current_price)
            
            # Pause before next iteration
            time.sleep(60)
        except Exception as e:
            print(f"Error in trading loop: {e}")
            time.sleep(60)

# Start the trading loop
start_trading_loop()
