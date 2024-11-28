import time
from datetime import datetime
from utils.fetch_data import fetch_data
from utils.calculations import calculate_slope, calculate_volatility
from utils.predictions import markov_prediction, apply_fuzzy_logic
from utils.genetic_algorithm import genetic_algorithm
from utils.trading import make_trade

def main():
    stock_symbol = input("Enter stock symbol: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    current_state = 'STABLE'
    while True:
        try:
            stock_data = fetch_data(stock_symbol, start_date, end_date)
            close_prices = [item['close'] for item in stock_data]

            slope = calculate_slope(close_prices)
            volatility = calculate_volatility(close_prices)

            if not slope or not volatility:
                print("Insufficient data, retrying...")
                time.sleep(60)
                continue

            next_state = markov_prediction(current_state)
            signal = apply_fuzzy_logic(slope, volatility, next_state)
            current_price = close_prices[-1]

            make_trade(signal, current_price)
            current_state = next_state

            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
