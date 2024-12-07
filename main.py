import time
from datetime import datetime
from utils.fetch_data import fetch_data
from utils.calculations import calculate_slope, calculate_volatility
from utils.predictions import markov_prediction, apply_fuzzy_logic
from utils.trading import make_trade
from data.start import validateUser
import data.data_extraction as extraction

import sys

sys.path.insert(0, './utils')

def main():

    if validateUser() == True:

        stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        print("Select a stock symbol from the following list:")
        for i, symbol in enumerate(stock_symbols, 1):
            print(f"{i}. {symbol}")
        choice = int(input("Enter the number corresponding to the stock symbol: "))
        stock_symbol = stock_symbols[choice - 1]
        current_state = 'STABLE'
        try:

            stock_data = extraction.data_two_months(stock_symbol)
            if not stock_data:
                print("NO data was fetched!\nExiting")

            close_prices = [stock_data[i]["close"] for i in range(len(stock_data))]
            slope = calculate_slope(close_prices)
            volatility = calculate_volatility(close_prices)
            print(volatility)
            print(slope)

            if not slope or not volatility:
                print("Insufficient data, retrying...")
                time.sleep(60)
            next_state = markov_prediction(current_state)
            print(next_state)
            signal = apply_fuzzy_logic(slope, volatility,next_state)
            current_price = close_prices[-1]

            make_trade(signal, current_price, 2)
            # Verification with today's trend
            extraction.fetch_data_for_today(stock_symbol)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
