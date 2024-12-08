import time
from datetime import datetime
from utils.fetch_data import fetch_data
from utils.calculations import calculate_slope, calculate_volatility, normalize_volume, calculate_RSI, calculate_moving_average_slope
from utils.predictions import markov_prediction, apply_fuzzy_logic
from utils.trading import make_trade
from data.start import validateUser
import data.data_extraction as extraction

import sys

sys.path.insert(0, './utils')

def main():

    # if validateUser() == True:
    check = input("Do you wan to continue: ")
    
    while(check == "y"):
        
        # stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        stock_symbol = input("Enter the stock symbol: ")
        current_state = 'STABLE'
        try:
            stock_data = extraction.analyze_data(stock_symbol)
            # ! Volume of the data
            volume = [stock_data[i]["volume"] for i in range(len(stock_data))]
            minVolume = min(volume)
            maxVolume = max(volume)
            avg_volume = normalize_volume(volume[-1], minVolume, maxVolume);
            # ! RSI of the data
            close_prices = [stock_data[i]["close"] for i in range(len(stock_data))]
            RSI = calculate_RSI(close_prices)
            # ! Moving average slope
            moving_average_slope = calculate_moving_average_slope(close_prices)
            
            if not stock_data:
                print("NO data was fetched!\nExiting")
            slope = calculate_slope(close_prices)
            volatility = calculate_volatility(close_prices)
            if not slope or not volatility:
                print("Insufficient data, retrying...")
                time.sleep(60)
            next_state = markov_prediction(current_state)
            print("\033[93m--------------------------------------------------\033[0m")
            print("Volatility: ", volatility)  # ! volatility
            print("Slope: ", slope)  # ! slope
            print("Next State: ", next_state)  # ! next state
            print("\033[93m--------------------------------------------------\033[0m")
            action = apply_fuzzy_logic(slope, volatility, next_state)
            # action, signal_value = apply_fuzzy_logic(slope, volatility, next_state, avg_volume, RSI, moving_average_slope)
            
            current_price = close_prices[-1]
            make_trade(action, current_price)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
        check = input("Do you wan to continue: ")


if __name__ == "__main__":
    main()
