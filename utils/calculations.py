import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

def calculate_slope(prices):
    if len(prices) < 2:
        return float('nan')
    x = np.arange(len(prices))
    try:
        slope, _, _, _, _ = linregress(x, prices)
        return slope
    except ValueError:
        return float('nan')

def calculate_volatility(prices):
    if len(prices) < 2:
        return float('nan')
    return np.std(np.diff(prices))

def predict_missing_values(prices):
    if len(prices) < 2:
        return prices

    valid_prices = [(i, price) for i, price in enumerate(prices) if price is not None]
    if len(valid_prices) < 2:
        return prices

    x = np.array([i for i, _ in valid_prices]).reshape(-1, 1)
    y = np.array([price for _, price in valid_prices])
    model = LinearRegression().fit(x, y)

    for i in range(len(prices)):
        if prices[i] is None:
            prices[i] = model.predict([[i]])[0]

    return prices
