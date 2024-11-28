import random
from ..config import MARKOV_MATRIX

def markov_prediction(current_state):
    probabilities = MARKOV_MATRIX[current_state]
    next_state = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    return next_state

def apply_fuzzy_logic(slope, volatility, next_state):
    if next_state == 'UP' and slope > 0.1 and volatility < 0.05:
        return 'BUY'
    elif next_state == 'DOWN' and slope < -0.1 and volatility > 0.05:
        return 'SELL'
    else:
        return 'HOLD'
