import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystem, ControlSystemSimulation
from config import MARKOV_MATRIX

def predict_state(stock_data):
    """ 
    find the current state of the data with the help of the last 2 month data (stock_data)
    """
    # Calculate the average closing price for the last 2 months
    avg_close_price = sum([day["close"] for day in stock_data]) / len(stock_data)
    # Get the current closing price
    current_close_price = stock_data[-1]["close"]
    # Calculate the percentage change in price
    price_change = (current_close_price - avg_close_price) / avg_close_price
    # Define the state based on the price change
    if price_change > 0.02:
        return "UP"
    elif price_change < -0.02:
        return "DOWN"
    else:
        return "STABLE"
    

def markov_prediction(current_state):
    """Predicts the next state using Markov's model.

    Args:
        current_state (str): The current state of the market.

    Returns:
        str: The predicted next state.
    """
    probabilities = MARKOV_MATRIX[current_state]
    next_state = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    return next_state

def normalize_rsi(rsi_value):
    """Normalize RSI value to be between 0 and 1."""
    # Ensure rsi_value is a float or int, not a string
    if isinstance(rsi_value, (float, int)):
        return min(max(rsi_value / 100, 0), 1)
    else:
        raise ValueError(f"Expected a numerical value for RSI, got {type(rsi_value)} instead.")

def apply_fuzzy_logic(slope_value, volatility_value, next_state , avg_volume_value, rsi_value, moving_avg_value, trend_today):
    """
    Predicts stock action (BUY, SELL, or HOLD) using fuzzy logic based on various indicators.

    Args:
        slope_value (float): The slope of the stock prices (trend direction).
        volatility_value (float): The volatility of the stock prices (market risk).
        rsi_value (float): The Relative Strength Index (RSI) value.
        moving_avg_value (float): The moving average of the stock prices.
        avg_volume_value (float): The average volume of trades.
        next_state (str): The predicted next state of the market (e.g., "UP", "DOWN", "STABLE").

    Returns:
        str: Suggested action ("BUY", "SELL", or "HOLD").
        float: Signal value (0 to 1).
    """
    # Normalize RSI value to be between 0 and 1
    rsi_value = float(rsi_value)
    rsi_value = normalize_rsi(rsi_value)
    
    print("Normalized RSI: ", rsi_value)

    # Define fuzzy variables
    slope = Antecedent(np.arange(-1, 1.1, 0.1), 'slope')
    volatility = Antecedent(np.arange(0, 1.1, 0.1), 'volatility')
    rsi = Antecedent(np.arange(0, 1.1, 0.1), 'rsi')
    moving_avg = Antecedent(np.arange(-1, 1.1, 0.1), 'moving_avg')
    avg_volume = Antecedent(np.arange(0, 1.1, 0.1), 'avg_volume')
    signal = Consequent(np.arange(0, 1.1, 0.1), 'signal')

    # Define membership functions for slope
    slope['downward'] = fuzz.trimf(slope.universe, [-1, -0.6, -0.2])
    slope['flat'] = fuzz.trimf(slope.universe, [-0.3, 0, 0.05])
    slope['upward'] = fuzz.trimf(slope.universe, [0.1, 0.6, 1])

    # Define membership functions for volatility
    volatility['low'] = fuzz.trimf(volatility.universe, [0, 0, 0.2])
    volatility['medium'] = fuzz.trimf(volatility.universe, [0.1, 0.45, 0.7])
    volatility['high'] = fuzz.trimf(volatility.universe, [0.6, 1, 1])

    # Define membership functions for RSI
    rsi['oversold'] = fuzz.trimf(rsi.universe, [0, 0, 0.3])
    rsi['neutral'] = fuzz.trimf(rsi.universe, [0.25, 0.5, 0.75])
    rsi['overbought'] = fuzz.trimf(rsi.universe, [0.7, 1, 1])

    # Define membership functions for moving average
    moving_avg['below'] = fuzz.trimf(moving_avg.universe, [-1, -0.6, 0])
    moving_avg['at'] = fuzz.trimf(moving_avg.universe, [-0.1, 0, 0.1])
    moving_avg['above'] = fuzz.trimf(moving_avg.universe, [0, 0.6, 1])

    # Define membership functions for average volume
    avg_volume['low'] = fuzz.trimf(avg_volume.universe, [0, 0, 0.4])
    avg_volume['medium'] = fuzz.trimf(avg_volume.universe, [0.3, 0.5, 0.7])
    avg_volume['high'] = fuzz.trimf(avg_volume.universe, [0.6, 1, 1])

    # Define membership functions for signal
    signal['sell'] = fuzz.trimf(signal.universe, [0, 0, 0.3])
    signal['hold'] = fuzz.trimf(signal.universe, [0.2, 0.5, 0.5])
    signal['buy'] = fuzz.trimf(signal.universe, [0.4, 1, 1])

    # Define fuzzy rules
    rules = [
        Rule(slope['downward'] & volatility['high'], signal['sell']),
        Rule(slope['downward'] & volatility['medium'], signal['sell']),
        Rule(slope['upward'] & rsi['oversold'], signal['buy']),
        Rule(slope['upward'] & volatility['low'], signal['buy']),
        Rule(slope['flat'] & rsi['neutral'], signal['hold']),
        Rule(slope['flat'] & volatility['medium'], signal['hold']),
        Rule(slope['downward'] & rsi['oversold'], signal['hold']),
        Rule(slope['upward'] & rsi['overbought'], signal['sell']),
        Rule(slope['flat'] & avg_volume['medium'], signal['buy']),
        Rule(slope['upward'] & avg_volume['low'], signal['hold']),
        Rule(slope['downward'] & avg_volume['high'], signal['sell']),
        Rule(rsi['oversold'] & slope['upward'] & moving_avg['above'], signal['buy']),
        Rule(rsi['overbought'], signal['sell']),
        Rule(rsi['neutral'] & slope['flat'], signal['hold']),
        Rule(rsi['oversold'] & moving_avg['below'], signal['buy']),
        Rule(moving_avg['above'] & avg_volume['high'], signal['buy']),
        Rule(moving_avg['below'] & avg_volume['low'], signal['sell']),
        Rule(moving_avg['at'] & avg_volume['medium'], signal['hold']),
        Rule(moving_avg['at'] & rsi['neutral'], signal['hold']),
        Rule(moving_avg['below'] & volatility['medium'], signal['sell']),
        Rule(moving_avg['above'] & volatility['low'], signal['buy']),
        Rule(avg_volume['low'] & rsi['oversold'], signal['buy']),
        Rule(avg_volume['high'] & rsi['overbought'], signal['sell']),
        Rule(avg_volume['medium'] & slope['flat'], signal['hold']),
        Rule(volatility['low'] & slope['upward'], signal['buy']),
        Rule(volatility['high'] & rsi['neutral'], signal['hold']),
        Rule(volatility['medium'] & rsi['oversold'], signal['buy']),
        Rule(volatility['low'] & rsi['overbought'], signal['sell']),
        Rule(volatility['medium'] & moving_avg['above'], signal['buy']),
        Rule(volatility['medium'] & moving_avg['below'], signal['sell']),
        Rule(volatility['high'] & slope['downward'], signal['sell']),
    ]

    # Create a fuzzy control system
    stock_ctrl = ControlSystem(rules)
    stock_sim = ControlSystemSimulation(stock_ctrl)

    # Set input values
    stock_sim.input['slope'] = slope_value
    stock_sim.input['volatility'] = volatility_value
    stock_sim.input['rsi'] = rsi_value
    stock_sim.input['moving_avg'] = moving_avg_value
    stock_sim.input['avg_volume'] = avg_volume_value

    # Compute output
    stock_sim.compute()

    # Get output value
    signal_value = stock_sim.output['signal']

    # Use next_state to adjust the action based on the signal
    print("Signal Value: ", signal_value)
    print(trend_today)
    if next_state == 'UP':
        if signal_value > 0.55:
            action = "BUY" 
        elif signal_value < 0.3:
            action = "SELL"
        else:
            if trend_today == "BUY":
                action = "BUY"
            elif trend_today == "SELL":
                action = "SELL"
            else:
                action = "HOLD"

    elif next_state == 'DOWN':
        if signal_value < 0.45:
            action = "SELL"
        elif signal_value > 0.7:
            action = "BUY"
        else:
            if trend_today == "BUY":
                action = "BUY"
            elif trend_today == "SELL":
                action = "SELL"
            else:
                action = "HOLD"

    else:  # Neutral state
        if signal_value < 0.5:
            action = "SELL" if trend_today == "SELL" else "HOLD"
        elif 0.5 <= signal_value < 0.6:
            action = "HOLD"
        else:
            action = "BUY" if trend_today == "BUY" else "HOLD"

    print("Action: ", action)

    return action, signal_value

if __name__ == "__main__":
    # Example usage
    test_cases = [
        {'slope': 0.8, 'volatility': 0.2, 'rsi': 25, 'moving_avg': 0.5, 'avg_volume': 0.7, 'next_state': 'UP'},
        {'slope': -0.7, 'volatility': 0.9, 'rsi': 75, 'moving_avg': -0.4, 'avg_volume': 0.3, 'next_state': 'DOWN'},
        {'slope': 0.0, 'volatility': 0.5, 'rsi': 50, 'moving_avg': 0.0, 'avg_volume': 0.5, 'next_state': 'STABLE'},
    ]
    
    for test in test_cases:
        action, signal = apply_fuzzy_logic(
            test['slope'], test['volatility'], test['rsi'],
            test['moving_avg'], test['avg_volume'], test['next_state']
        )
        print(f"Action: {action}, Signal: {signal}")
