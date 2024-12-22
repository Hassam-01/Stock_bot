from collections import deque


# Function to recommend investment based on constraints
def recommended_action_BUY( ticker, price_of_stock, net_worth,signal_value):
    """
    :param ticker : AAPL, GOOGL, MSFT
    :param price of stock: price per stock
    :param net_worth : Total Balance
    :param signal_value : value of the trade signal (BUY or SELL)
    :return investment recommendation
    """

    # Variables:
    # 1. confidence_level: The level of confidence in the buy signal, which is based on the signal_value.
    # 2. investment_domains: A deque that holds the possible investment percentages based on confidence_level.
    # 3. recommended_investment: The amount of net_worth to invest, calculated by multiplying net_worth with the appropriate percentage from investment_domains.
    # 4. stocks_num: The number of stocks to buy, calculated based on recommended_investment divided by price_of_stock.
    # 5. stocks_investment: The total amount of money required to buy the recommended number of stocks (stocks_num * price_of_stock).

    if price_of_stock > net_worth :
        return "Investment not recommended. You have low balance brother"

    # Calculate the confidence level based on the signal value
    confidence_level = signal_value

    # Domain for investment based on confidence level
    investment_domains = deque()  # This will hold the possible investment percentages

    # Domains:
    # 1. confidence_level > 0.8: Invest 20% of net_worth.
    # 2. 0.6 < confidence_level <= 0.8: Invest 10% of net_worth.
    # 3. 0.4 < confidence_level <= 0.6: Invest 5% of net_worth.
    # 4. confidence_level <= 0.4: Invest 2% of net_worth.

    # Apply constraints based on the confidence level
    if confidence_level > 0.8:# represents a high BUY signal
        investment_domains.append(0.20)  # Invest 20% of net worth
    elif confidence_level > 0.6:# intermidiate BUY signal
        investment_domains.append(0.10)  # Invest 10% of net worth
    elif confidence_level >= 0.4:#weak BUY signal
        investment_domains.append(0.05)  # Invest 5% of net worth
    elif confidence_level < 0.4:#weak signal BUY
        investment_domains.append(0.02)  # Invest 2% of net worth


    # Constraint 1: Investment cannot exceed networth
    recommended_investment = net_worth * investment_domains[0]


    #Constraint 2: The investment cannot exceed the recommended investment
    stocks_num = int(recommended_investment // price_of_stock)
    stocks_investment = stocks_num * price_of_stock

    # Final Decision: Investment recommendation within bounds
    if stocks_investment <= net_worth and stocks_investment > price_of_stock:
        return f" ${stocks_investment:.2f}, BUY {stocks_num} of stocks of {ticker}"

    else:
        return "Investment exceeds available funds. Recommend not to spend."





def recommended_action_SELL(ticker,stocks_owned,price_of_stock,signal_value,purchase_price):
    """
    :param ticker: APPL, GOOGL ,MSFT
    :param stocks_owned: number of stocks owned
    :param price_of_stock : price per stock
    :param signal_value : the value of the signal
    :param purchase_price : the price of purchase
    :return: selling recommendations
    """

    # sell signal is strongest when is closer to 0 and decreases when it's approaching 0.3



    # Variables:
    # 1. Profit percentage (based on price increase)
    # 2. Number of stocks to sell (subset of stocks_owned)
    # 3. Signal strength (value influencing sell decision)

    profit_percentage = ((price_of_stock - purchase_price) / purchase_price) * 100
    stocks_to_sell = deque()  # Domain for number of stocks to sell


    # Constraint 1: Price of stock should have increased enough to make a profit
    if profit_percentage >= 30:  # A significant profit margin (40% increase in price)
        if signal_value <= 0.2:  # Strong SELL signal
            stocks_to_sell.append(int(stocks_owned * 0.4))  # Sell 40% of stocks
        elif signal_value <= 0.3:  # Moderate SELL signal
            stocks_to_sell.append(int(stocks_owned * 0.2))  # Sell 20% of stocks
        else:  # Weak SELL signal
            stocks_to_sell.append(int(stocks_owned * 0.1))  # Sell 10% of stocks

    else:  # Constraint 2: If profit is not significant, recommend minimal selling
        if signal_value <= 0.3:  #  SELL signal but low profit
            stocks_to_sell.append(int(stocks_owned * 0.1))  # Sell 10% of stocks
        else:
            stocks_to_sell.append(int(stocks_owned * 0.1))#sell 5% of stocks

    # Constraint 3: Ensure at least one stock is sold if possible
    if stocks_owned <= 1:
        return f"No stocks of {ticker} available to sell."

    # Step 3: Final decision
    recommended_stocks = stocks_to_sell[0] if stocks_to_sell else 0
    revenue = recommended_stocks * price_of_stock  # Calculate revenue from selling

    return f"SELL {recommended_stocks} stocks of {ticker} at ${price_of_stock:.2f} per stock, generating ${revenue:.2f} revenue."



if __name__ == "__main__" :
    print(recommended_action_BUY(
        ticker="AAPL",
        price_of_stock=150,
        net_worth=5000,
        signal_value=0.9  # High confidence in BUY signal
    ))
    print(recommended_action_BUY(
        ticker="GOOGL",
        price_of_stock=2500,
        net_worth=10000,
        signal_value=0.7  # Intermediate confidence in BUY signal
    ))
    print(recommended_action_BUY(
        ticker="MSFT",
        price_of_stock=300,
        net_worth=20000000,
        signal_value=0.3  # Weak BUY signal
    ))
    print(recommended_action_BUY(
        ticker="AAPL",
        price_of_stock=4000,
        net_worth=1000,
        signal_value=0.85  # High confidence in BUY signal
    ))
    print(recommended_action_SELL(
        ticker="AAPL",
        stocks_owned=100,
        price_of_stock=200,
        signal_value=0.9,  # High SELL signal
        purchase_price=100
    ))

    print(recommended_action_SELL(
        ticker="GOOGL",
        stocks_owned=50,
        price_of_stock=1800,
        signal_value=0.6,  # Moderate SELL signal
        purchase_price=1500
    ))
    print(recommended_action_SELL(
        ticker="MSFT",
        stocks_owned=30,
        price_of_stock=300,
        signal_value=0.3,  # Low SELL signal
        purchase_price=290
    ))
    print(recommended_action_SELL(
        ticker="AMZN",
        stocks_owned=200,
        price_of_stock=3500,
        signal_value=0.95,  # Very strong SELL signal
        purchase_price=2000
    ))


