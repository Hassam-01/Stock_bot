# plotData.py
import matplotlib.pyplot as plt

def plot_data(timestamps, open_prices, close_prices, predictions=None):
    plt.figure(figsize=(10, 6))

    # Plotting open and close prices
    plt.plot(timestamps, open_prices, label="Open Prices", color='blue')
    plt.plot(timestamps, close_prices, label="Close Prices", color='red')

    if predictions:
        plt.plot(timestamps, predictions, label="Predictions", color='green', linestyle='--')

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Stock Prices and Predictions')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_predictions(timestamps, predictions):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, predictions, label="Predictions", color='green', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Prediction')
    plt.title('Predicted Values')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
