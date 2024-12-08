import random
from config import MARKOV_MATRIX
import numpy as np
import skfuzzy as fuzz
from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystem, ControlSystemSimulation


def markov_prediction(current_state):
    """Predicts the next state using markov's model
        Args:
            current_state(str) : the current state of the market
        return:
            returns the next state(str)
    """
    probabilities = MARKOV_MATRIX[current_state]
    next_state = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    return next_state

def apply_fuzzy_logic(slope_value, volatility_value,next_state):
    """
        Predicts stock action (BUY, SELL, or HOLD) using fuzzy logic based on slope, volatility, and next state.

        Args:
            slope_value (float): The slope of the stock prices (trend direction).
            volatility_value (float): The volatility of the stock prices (market risk).
            next_state (str): The predicted next state of the market (e.g., "UP", "DOWN", "STABLE").

        Returns:
            str: Suggested action ("BUY", "SELL", or "HOLD").
            float: Signal value (0 to 1).
        """
    # Define fuzzy variables
    slope = Antecedent(np.arange(-1, 1.1, 0.1), 'slope')
    volatility = Antecedent(np.arange(0, 1.1, 0.1), 'volatility')
    signal = Consequent(np.arange(0, 1.1, 0.1), 'signal')

    # Define membership functions for slope
    slope['downward'] = fuzz.trimf(slope.universe, [-1, -0.6, -0.2])
    slope['flat'] = fuzz.trimf(slope.universe, [-0.3, 0, 0.3])
    slope['upward'] = fuzz.trimf(slope.universe, [0.2, 0.6, 1])


    # Define membership functions for volatility
    volatility['low'] = fuzz.trimf(volatility.universe, [0, 0, 0.25])
    volatility['medium'] = fuzz.trimf(volatility.universe, [0.2, 0.45, 0.7])
    volatility['high'] = fuzz.trimf(volatility.universe, [0.6, 1, 1])

    # Define membership functions for signal
    signal['sell'] = fuzz.trimf(signal.universe, [0, 0, 0.5])
    signal['hold'] = fuzz.trimf(signal.universe, [0.4, 0.5, 0.6])
    signal['buy'] = fuzz.trimf(signal.universe, [0.5, 1, 1])

    # Define fuzzy rules (without next_state in the fuzzy rule combination)
    rule1 = Rule(slope['downward'] & volatility['medium'], signal['sell'])
    rule2 = Rule(slope['downward'] & volatility['high'], signal['sell'])
    rule3 = Rule(slope['flat'] & volatility['high'], signal['sell'])
    rule4 = Rule(slope['downward'] & volatility['low'], signal['sell'])
    rule5 = Rule(slope['upward'] & volatility['low'], signal['buy'])
    rule6 = Rule(slope['upward'] & volatility['medium'], signal['buy'])
    rule7 = Rule(slope['flat'] & volatility['low'], signal['buy'])
    rule8 = Rule(slope['flat'] & volatility['medium'], signal['hold'])


    # Create a fuzzy control system
    stock_ctrl = ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6,rule7,rule8])
    stock_sim = ControlSystemSimulation(stock_ctrl)

    # Set input values
    stock_sim.input['slope'] = slope_value
    stock_sim.input['volatility'] = volatility_value

    # Compute output
    stock_sim.compute()

    # Get output value
    signal_value = stock_sim.output['signal']
    print(signal_value)

    # Use next_state to adjust the action based on the signal
    if next_state == 'UP':
        if signal_value > 0.6:  # Lowered threshold for "BUY"
            action = "BUY"
        elif signal_value < 0.4:  # Raised threshold for "SELL"
            action = "SELL"
        else:
            action = "HOLD"

    elif next_state == 'DOWN':
        if signal_value < 0.3:
            action = "SELL"
        elif signal_value > 0.8:
            action = "BUY"
        else:
            action = "HOLD"
    else:
        # If next_state is STABLE, use the signal as is
        if signal_value < 0.4:
            action = "SELL"
        elif 0.4 <= signal_value < 0.7:
            action = "HOLD"
        else:
            action = "BUY"

    return action
if __name__ == "__main__":
    # Example usage
    test_cases = [
        {'slope': 0.8, 'volatility': 0.2, 'next_state': 'UP'},
        {'slope': -0.7, 'volatility': 0.9, 'next_state': 'DOWN'},
        {'slope': 0.0, 'volatility': 0.5, 'next_state': 'STABLE'},
    ]
    for test in test_cases:
        print(apply_fuzzy_logic(test['slope'], test['volatility'], test['next_state']))