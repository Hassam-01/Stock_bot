from collections import deque

SIGNAL_WEAK = 0.4
SIGNAL_MODERATE = 0.6
SIGNAL_STRONG = 0.8
PROFIT_HIGH = 30  # 30%
PROFIT_MODERATE = 10  # 10%
PROFIT_VERY_HIGH = 70  # 70% - new threshold
VOLATILITY_HIGH = 0.6
VOLATILITY_LOW = 0.1
INVESTMENT_MIN_PERCENT = 0.05
INVESTMENT_WARNING_PERCENT = 0.10

def adjust_signal(signal: float, volatility: float, adjustment_type: str = "buy") -> float:
    if adjustment_type == "buy":
        return signal * (1 - volatility)
    elif adjustment_type == "sell":
        return signal * (1 + volatility)
    return signal

def recommended_action_SELL(
    ticker: str, 
    stocks_owned: int, 
    price_of_stock: float, 
    signal_value: float, 
    purchase_price: float, 
    volatility: float, 
    risk_tolerance: str = "medium"
) -> dict:
    if stocks_owned <= 0:
        return {"message": f"No stocks of {ticker} available to sell."}
    if purchase_price <= 0:
        return {"message": "Invalid purchase price."}

    profit_percentage = ((price_of_stock - purchase_price) / purchase_price) * 100
    adjusted_signal = adjust_signal(signal_value, volatility, "sell")
    risk_factor = {"low": 0.5, "medium": 1.0, "high": 1.5}.get(risk_tolerance, 1.0)
    stocks_to_sell = 0
    recommendation_reason = "No specific recommendation"

    # Very high profit condition (70%+) with low volatility - aggressive sell
    if profit_percentage >= PROFIT_VERY_HIGH and volatility <= VOLATILITY_LOW:
        stocks_to_sell = int(stocks_owned * 0.8 * risk_factor)
        recommendation_reason = f"Very high profit ({profit_percentage:.1f}%) with low volatility - recommend taking profits"
    
    elif profit_percentage >= PROFIT_HIGH:
        if volatility <= VOLATILITY_LOW:
            stocks_to_sell = int(stocks_owned * 0.6 * risk_factor)
            recommendation_reason = f"High profit ({profit_percentage:.1f}%) with low volatility"
        else:
            stocks_to_sell = int(stocks_owned * 0.5 * risk_factor if adjusted_signal <= 0.2 else stocks_owned * 0.3)
            recommendation_reason = f"High profit ({profit_percentage:.1f}%) target reached"
    
    elif volatility <= VOLATILITY_LOW and signal_value <= SIGNAL_WEAK:
        stocks_to_sell = int(stocks_owned * 0.4 * risk_factor)
        recommendation_reason = "Low volatility environment - minimal price movement expected"
    
    elif profit_percentage >= PROFIT_MODERATE:
        if volatility <= VOLATILITY_LOW:
            stocks_to_sell = int(stocks_owned * 0.3 * risk_factor)
            recommendation_reason = "Moderate profit with low volatility"
        else:
            stocks_to_sell = int(stocks_owned * 0.2 * risk_factor if adjusted_signal <= 0.3 else stocks_owned * 0.1)
            recommendation_reason = "Moderate profit target reached"

    if volatility > VOLATILITY_HIGH and stocks_to_sell > 0:
        stocks_to_sell = max(1, int(stocks_to_sell * 0.5))
        recommendation_reason += " (reduced due to high volatility)"

    if stocks_to_sell > 0:
        revenue = stocks_to_sell * price_of_stock
        return {"message": (f"SELL RECOMMENDATION for {ticker}:\n"
                          f"Number of shares to sell: {stocks_to_sell}\n"
                          f"Expected revenue: ${revenue:,.2f}\n"
                          f"Profit percentage: {profit_percentage:.1f}%\n"
                          f"Volatility-adjusted signal: {adjusted_signal:.2f}\n"
                          f"Current volatility: {volatility:.2f}\n"
                          f"Reason: {recommendation_reason}")}
    else:
        return {"message": f"Sale not recommended for {ticker}. Insufficient profit or unfavorable conditions."}

def recommended_action_BUY(
    ticker: str, 
    price_of_stock: float, 
    net_worth: float, 
    signal_value: float, 
    volatility: float, 
    risk_tolerance: str = "medium"
) -> dict:
    if price_of_stock > net_worth:
        return {"message": f"Investment not recommended. You have low balance."}

    investment_percentage = (price_of_stock / net_worth) * 100
    adjusted_signal = adjust_signal(signal_value, volatility, "buy")
    risk_factor = {"low": 0.5, "medium": 1.0, "high": 1.5}.get(risk_tolerance, 1.0)
    investment = 0
    caution_flag = ""

    if INVESTMENT_MIN_PERCENT * 100 <= investment_percentage <= INVESTMENT_WARNING_PERCENT * 100:
        investment = 0.05
        caution_flag = " (CAUTION: Investment is between 5-10% of net worth)"
    elif adjusted_signal >= SIGNAL_STRONG:
        investment = 0.20 * risk_factor
    elif adjusted_signal >= SIGNAL_MODERATE:
        investment = 0.10 * risk_factor
    elif adjusted_signal >= SIGNAL_WEAK:
        if volatility <= VOLATILITY_LOW:
            investment = 0.08 * risk_factor
        else:
            investment = 0.05 * risk_factor
    else:
        if volatility <= VOLATILITY_LOW:
            investment = 0.04 * risk_factor
        else:
            investment = 0.02 * risk_factor

    if volatility > VOLATILITY_HIGH:
        investment *= 0.5
        caution_flag += " (reduced due to high volatility)"

    recommended_investment = net_worth * investment

    if recommended_investment < price_of_stock:
        return {"message": f"The stock price (${price_of_stock:,.2f}) is more than {investment * 100:.1f}% of your net worth (${net_worth:,.2f})."}

    stocks_to_buy = int(recommended_investment // price_of_stock)
    total_investment = stocks_to_buy * price_of_stock

    if total_investment <= net_worth and stocks_to_buy > 0:
        return {"message": (f"BUY RECOMMENDATION for {ticker}:\n"
                          f"Number of shares to buy: {stocks_to_buy}\n"
                          f"Total investment: ${total_investment:,.2f}\n"
                          f"Signal strength: {adjusted_signal:.2f}\n"
                          f"Current volatility: {volatility:.2f}\n"
                          f"Investment recommendation based on signal and volatility analysis{caution_flag}")}
    else:
        return {"message": "Investment exceeds available funds or insufficient funds for even one stock."}
if __name__ == "__main__":
    print(recommended_action_SELL(
        ticker="AAPL",
        stocks_owned=3,
        price_of_stock=253.48,
        signal_value=0.44,  # High confidence in BUY signal
        purchase_price=147,
        # net_worth=4381
        volatility=0.04  # Low volatility
    ))
    # buy
    print(recommended_action_BUY(
        ticker="AAPL",
        price_of_stock=253.48,
        net_worth=4381,
        signal_value=0.44,  # High confidence in BUY signal
        volatility=0.04  # Low volatility
    ))
    print(recommended_action_SELL(
        ticker="GOOGL",
        stocks_owned=50,
        price_of_stock=1800,
        signal_value=0.3,  # Moderate SELL signal
        purchase_price=1500,
        volatility=0.4  # Moderate volatility
    ))

    print(recommended_action_SELL(
        ticker="MSFT",
        stocks_owned=30,
        price_of_stock=300,
        signal_value=0.1,  # Low SELL signal
        purchase_price=290,
        volatility=0.7  # High volatility
    ))
