import os

API_KEY = os.getenv('9a19db152424baf1aa1e20de497d038a0997ba45')
VALID_STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'FB', 'NVDA', 'AMD', 'SPY']

MARKOV_MATRIX = {
    'UP': {'UP': 0.6, 'DOWN': 0.3, 'STABLE': 0.1},
    'DOWN': {'UP': 0.2, 'DOWN': 0.5, 'STABLE': 0.3},
    'STABLE': {'UP': 0.3, 'DOWN': 0.3, 'STABLE': 0.4}
}

GENE_POOL = [0.2, 0.3, 0.4, -0.2, -0.3, -0.4]
BEST_GENES = {'BUY_THRESHOLD': 0.3, 'SELL_THRESHOLD': -0.3}
