# import time
# from datetime import datetime
# from utils.fetch_data import fetch_data
# from utils.calculations import calculate_slope, calculate_volatility, normalize_volume, calculate_RSI, \
#     calculate_moving_average_slope
# from utils.predictions import markov_prediction, apply_fuzzy_logic
# from utils.trading import make_trade
# from data.start import validateUser
# import data.data_extraction as extraction
# from utils.recommendations import recommended_action_BUY,recommended_action_SELL
# import sys

# sys.path.insert(0, './utils')


# def main():
#     # if validateUser() == True:
#     check = input("Do you wan to continue: ")

#     while (check == "y"):

#         # stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
#         stock_symbol = input("Enter the stock symbol: ")
#         current_state = 'STABLE'
#         try:
#             stock_data, trade_date, trade_price, five_days_trend, common_signal = extraction.analyze_data(stock_symbol)
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
#             action, signal_value = apply_fuzzy_logic(slope, volatility, next_state, avg_volume, RSI,
#                                                      moving_average_slope, common_signal)
#!             current_price = close_prices[-1]
#!             if (action == "BUY"):
#!                 recommended = recommended_action_BUY(ticker=stock_symbol, stock_price=current_price,
#!                                                      net_worth=1500000,
#!                                                      signal_value=signal_value)
#!             elif (action == "SELL"):
#!                 recommended = recommended_action_SELL(ticker=stock_symbol, stock_price=current_price,
#!                                                       stocks_owned=10,
#!                                                       signal_value=signal_value, purchase_price=500)
#             else:
#                 recommended = "HOLD"
#             make_trade(action, current_price)
#             print(f"The recommended action is: {recommended}")


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
from utils.recommendations import recommended_action_BUY,recommended_action_SELL

app = FastAPI()

class RecommendationRequest(BaseModel):
    ticker: str
    stocks_owned: int = None
    purchase_price: float = None
    signal_value: float = None
    stock_price: float = None
    net_worth: float = None
    volatility: float = None
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stock-bot-web-client-hassam-alis-projects-909d02f3.vercel.app",
        "https://stock-bot-web-client-git-main-hassam-alis-projects-909d02f3.vercel.app",
        "https://stock-bot-web-client.vercel.app","http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/signal/recommendation")
def get_recommendation(request: RecommendationRequest):
    print(request, " HI")
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
                "volatility": volatility,
                "slope": slope,
                "RSI": RSI,
                "moving_avg": moving_average_slope,
                "avg_volume": avg_volume,
                "signal_value": signal_value, 
            },
            "five_days_trend_data": five_days_trend,
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")

@app.get("/")
async def read_root():
    return "Hello world"

@app.post("/api/trade/sell/recommendation")
def get_sell_trade_recommendation(request: RecommendationRequest):
    print(request)
    ticker = request.ticker.upper()
    stocks_owned = request.stocks_owned
    purchase_price = request.purchase_price
    signal_value = request.signal_value
    stock_price = request.stock_price
    volatility = request.volatility
    try:
        recommended = recommended_action_SELL(ticker, stocks_owned,stock_price, signal_value, purchase_price, volatility)
        print("recommended: ", recommended)
        return recommended
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")

@app.post("/api/trade/buy/recommendation")
def get_buy_trade_recommendation(request: RecommendationRequest):
    stock_price = request.stock_price
    net_worth = request.net_worth
    signal_value = request.signal_value
    ticker = request.ticker.upper()
    volatility  = request.volatility
    try:
        recommended = recommended_action_BUY(ticker, stock_price, net_worth, signal_value, volatility)
        return recommended
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)