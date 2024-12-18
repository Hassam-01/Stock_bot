# import time
# from datetime import datetime
# from utils.fetch_data import fetch_data
# from utils.calculations import calculate_slope, calculate_volatility, normalize_volume, calculate_RSI, calculate_moving_average_slope
# from utils.predictions import markov_prediction, apply_fuzzy_logic
# from utils.trading import make_trade
# from data.start import validateUser
# import data.data_extraction as extraction

# import sys

# sys.path.insert(0, './utils')

# def main():

#     # if validateUser() == True:
#     check = input("Do you wan to continue: ")
    
#     while(check == "y"):
        
#         # stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
#         stock_symbol = input("Enter the stock symbol: ")
#         current_state = 'STABLE'
#         try:
#             stock_data, trade_date, trade_price, five_days_trend = extraction.analyze_data(stock_symbol)
#             # ! Volume of the data
#             print("00")
#             volume = [stock_data[i]["volume"] for i in range(len(stock_data))]
#             print("01")
#             minVolume = min(volume)
#             print("02")
#             maxVolume = max(volume)
#             print("03")
#             avg_volume = normalize_volume(volume[-1], minVolume, maxVolume);
#             print("04")
#             # ! RSI of the data
#             close_prices = [stock_data[i]["close"] for i in range(len(stock_data))]
#             RSI = calculate_RSI(close_prices)
#             # ! Moving average slope
#             moving_average_slope = calculate_moving_average_slope(close_prices)
#             if not stock_data:
#                 print("NO data was fetched!\nExiting")
#             slope = calculate_slope(close_prices)
#             volatility = calculate_volatility(close_prices)
#             if not slope or not volatility:
#                 print("Insufficient data, retrying...")
#                 time.sleep(60)
#             next_state = markov_prediction(current_state)
#             print("\033[93m--------------------------------------------------\033[0m")
#             print("Volatility: ", volatility)  # ! volatility
#             print("Slope: ", slope)  # ! slope
#             print("Next State: ", next_state)  # ! next state
#             print("\033[93m--------------------------------------------------\033[0m")
#             print("\033[91m--------------------------------------------------\033[0m")
#             print("\033[95m--------------------------------------------------\033[0m")
#             # print RSI, Moving average slope, and average volume
#             print("RSI: ", RSI)
#             print("Moving Average Slope: ", moving_average_slope)
#             print("Average Volume: ", avg_volume)
#             print("\033[95m--------------------------------------------------\033[0m")
            
#             # action = apply_fuzzy_logic(slope, volatility, next_state)
#             action, signal_value = apply_fuzzy_logic(slope, volatility, next_state, avg_volume, RSI, moving_average_slope)
            
#             current_price = close_prices[-1]
#             make_trade(action, current_price)
#             print("last")
#         except Exception as e:
#             print(f"Error: {e}")
#             time.sleep(10)
#         check = input("Do you wan to continue: ")


# if __name__ == "__main__":
#     main()


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.calculations import calculate_slope, calculate_volatility, normalize_volume, calculate_RSI, calculate_moving_average_slope
from utils.predictions import markov_prediction, apply_fuzzy_logic, predict_state
import data.data_extraction as extraction

app = FastAPI()

class RecommendationRequest(BaseModel):
    ticker: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # For production, replace "*" with the React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recommendation")
def get_recommendation(request: RecommendationRequest):
    stock_symbol = request.ticker.upper()
    try:
        # Fetch and analyze stock data
        stock_data, trade_date, trade_price, five_days_trend, common_signal = extraction.analyze_data(stock_symbol)
        current_state = predict_state(stock_data)
        print("Current State: ", current_state)
        if not stock_data:
            raise HTTPException(status_code=404, detail="No data found for the stock symbol")

        volume = [stock_data[i]["volume"] for i in range(len(stock_data))]
        min_volume = min(volume)
        max_volume = max(volume)
        avg_volume = normalize_volume(volume[-1], min_volume, max_volume)
        close_prices = [stock_data[i]["close"] for i in range(len(stock_data))]
        RSI = calculate_RSI(close_prices)
        moving_average_slope = calculate_moving_average_slope(close_prices)
        slope = calculate_slope(close_prices)
        volatility = calculate_volatility(close_prices)
        next_state = markov_prediction(current_state)
        print("Next State: ", next_state)
        
        action, signal_value = apply_fuzzy_logic(slope, volatility, next_state, avg_volume, RSI, moving_average_slope,common_signal)
        # print("Five days trend from pyhton: ", five_days_trend)
        response = {
            # "signal": "SELL" if stock_symbol == "AAPL" else action,
            'signal': action,
            "trade_date": trade_date,
            "trade_price": trade_price,
            "predictionData": stock_data,
            "pythonData": {
                "Volatility": volatility,
                "Slope": slope,
                "RSI": RSI,
                "Moving Avg Slope": moving_average_slope,
                "Avergae Volume": avg_volume,
            },
            "five_days_trend_data": five_days_trend,
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")
