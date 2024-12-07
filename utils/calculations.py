import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression


def calculate_slope(prices):
    """
        Calculates the slope from the list of stock prices
        returns slope in the range [-1,1]
    """

    # returns zero if insufficient data
    if len(prices) < 2:
        return 0.0

    #arrage the list into a numpy array
    x = np.arange(len(prices))
    try:
        slope, _, _, _, _ = linregress(x, prices)

        # Use max of absolute slope or a minimum threshold
        max_slope = max(abs(slope), 5)

        # Normalize slope to the range [-1, 1]
        normalized_slope = max(-1.0, min(slope / max_slope, 1.0))
        return normalized_slope
    except ValueError:
        return 0.0


def calculate_volatility(prices):
    if len(prices) < 2:
        return 0.0  # Default to 0 if insufficient data

    # Use percentage differences for more consistent volatility measurement
    price_diff = np.diff(prices)
    relative_changes = price_diff / prices[:-1]
    raw_volatility = np.std(relative_changes)

    # Normalize volatility to the range [0, 1]
    max_volatility = 0.2  # Adjust based on dataset (e.g., 20% maximum volatility)
    normalized_volatility = min(raw_volatility / max_volatility, 1.0)
    return normalized_volatility


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
