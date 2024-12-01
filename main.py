import time
from datetime import datetime
from utils.fetch_data import fetch_data
from utils.calculations import calculate_slope, calculate_volatility
from utils.predictions import markov_prediction, apply_fuzzy_logic
from utils.trading import make_trade
from data.start import validateUser


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
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        max_trade = int(input("Enter the maximum number of trades you want to make: "))
        trade_count = 0
        current_state = 'STABLE'
        while trade_count < max_trade:
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

                trade_details = make_trade(signal, current_price, 2)
                if(trade_details["symbol"] != "HOLD"):
                    trade_count += 1
                current_state = next_state



                time.sleep(60)
                stock_data = []
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)


if __name__ == "__main__":
    main()
