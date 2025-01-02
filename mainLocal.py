import time
from datetime import datetime
from utils.fetch_data import fetch_data
from utils.calculations import calculate_slope, calculate_volatility, normalize_volume, calculate_RSI, \
    calculate_moving_average_slope
from utils.predictions import markov_prediction, apply_fuzzy_logic, predict_state
from utils.trading import make_trade
import data.data_extraction as extraction
from utils.recommendations import recommended_action_BUY, recommended_action_SELL
import sys

sys.path.insert(0, './utils')


def format_recommendation(recommendation):
    """Format the recommendation dictionary into a user-friendly string."""
    if isinstance(recommendation, dict):
        return recommendation.get('message', "No recommendation message provided.")
    return str(recommendation)

def get_user_input(prompt, cast_type=None):
    """Prompt user for input and cast it to the desired type."""
    while True:
        try:
            user_input = input(prompt)
            if cast_type:
                user_input = cast_type(user_input)
            return user_input
        except ValueError:
            print("Invalid input. Please try again.")

def main():
    print("\033[94mWelcome to the Stock Trading Bot!\033[0m")

    while True:
        continue_check = input("\033[93mDo you want to analyze stocks? (y/n): \033[0m").lower()
        if continue_check != 'y':
            print("\033[92mExiting the program. Goodbye!\033[0m")
            break

        stock_symbol = input("\033[96mEnter the stock symbol (e.g., AAPL, GOOGL): \033[0m").strip().upper()
        net_worth = get_user_input("\033[96mEnter your net worth: \033[0m", float)

        try:
            stock_data, trade_date, trade_price, five_days_trend, common_signal = extraction.analyze_data(stock_symbol)
            if not stock_data:
                print("\033[91mNo data was fetched!\033[0m\nExiting...")
                continue

            current_state = predict_state(stock_data)
            volume = [stock_data[i]["volume"] for i in range(len(stock_data))]
            minVolume = min(volume)
            maxVolume = max(volume)
            avg_volume = normalize_volume(volume[-1], minVolume, maxVolume)
            close_prices = [stock_data[i]["close"] for i in range(len(stock_data))]
            RSI = calculate_RSI(close_prices)
            moving_average_slope = calculate_moving_average_slope(close_prices)
            slope = calculate_slope(close_prices)
            volatility = calculate_volatility(close_prices)

            if not slope or not volatility:
                print("\033[91mInsufficient data, retrying after 60 seconds...\033[0m")
                time.sleep(60)
                continue

            next_state = markov_prediction(current_state)

            print("\033[93m--------------------------------------------------\033[0m")
            print(f"\033[96mVolatility: {volatility}\033[0m")
            print(f"\033[96mSlope: {slope}\033[0m")
            print(f"\033[96mNext State: {next_state}\033[0m")
            print("\033[93m--------------------------------------------------\033[0m")
            print(f"\033[96mRSI: {RSI}\033[0m")
            print(f"\033[96mMoving Average Slope: {moving_average_slope}\033[0m")
            print(f"\033[96mAverage Volume: {avg_volume}\033[0m")
            print("\033[93m--------------------------------------------------\033[0m")

            action, signal_value = apply_fuzzy_logic(slope, volatility, next_state, avg_volume, RSI,
                                                     moving_average_slope, common_signal)
            current_price = close_prices[-1]

            if action == "BUY":
                recommended = recommended_action_BUY(stock_symbol, current_price, net_worth, signal_value, volatility)
            elif action == "SELL":
                purchase_price = get_user_input(f"\033[96mEnter the price at which you purchased {stock_symbol}: \033[0m", float)
                stocks_owned = get_user_input(f"\033[96mEnter the number of {stock_symbol} stocks you own: \033[0m", int)
                print(current_price)
                recommended = recommended_action_SELL(stock_symbol, stocks_owned,current_price, signal_value, purchase_price, volatility)
            else:
                recommended = "HOLD"

            make_trade(action, current_price)
            formatedRecommend = format_recommendation(recommended)
            print(f"\033[92mThe recommended action is: {formatedRecommend}\033[0m")

        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            time.sleep(10)

if __name__ == "__main__":
    main()
