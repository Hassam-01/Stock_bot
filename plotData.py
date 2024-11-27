import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# Your raw data (use the data you provided)
# data = [
#     {'date': '2024-02-21T00:00:00.000Z', 'close': 142.55, 'high': 142.69, 'low': 140.675, 'open': 141.45, 'volume': 23315687},
#     {'date': '2024-02-22T00:00:00.000Z', 'close': 144.09, 'high': 145.0, 'low': 142.8, 'open': 144.93, 'volume': 27191892},
#     {'date': '2024-02-23T00:00:00.000Z', 'close': 143.96, 'high': 144.68, 'low': 143.43, 'open': 143.67, 'volume': 19493752},
#     # Add the remaining data here...
# ]


def plotData(data):
    # Convert the raw data into a DataFrame
    df = pd.DataFrame(data)

    # Convert the 'date' column to datetime for proper sorting if necessary
    df['date'] = pd.to_datetime(df['date'])

    # Plot the table using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed
    ax.axis('off')  # Turn off the axes
    tbl = table(ax, df, loc='center', colWidths=[0.2]*len(df.columns))  # Center align the table and adjust column widths
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 1.2)  # Scale the table for readability
    plt.show()

    # Plot graphs for Close and Open prices
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['close'], label='Close Price', color='blue', marker='o')
    plt.plot(df['date'], df['open'], label='Open Price', color='green', marker='x')
    plt.title('Close and Open Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot graphs for High and Low prices
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['high'], label='High Price', color='red', marker='o')
    plt.plot(df['date'], df['low'], label='Low Price', color='orange', marker='x')
    plt.title('High and Low Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot a bar graph for Volume
    plt.figure(figsize=(10, 6))
    plt.bar(df['date'], df['volume'], color='purple')
    plt.title('Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
# # Convert the raw data into a DataFrame
# df = pd.DataFrame(data)

# # Convert the 'date' column to datetime for proper sorting if necessary
# df['date'] = pd.to_datetime(df['date'])

# # Plot the table using matplotlib
# fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed
# ax.axis('off')  # Turn off the axes
# tbl = table(ax, df, loc='center', colWidths=[0.2]*len(df.columns))  # Center align the table and adjust column widths
# tbl.auto_set_font_size(False)
# tbl.set_fontsize(10)
# tbl.scale(1.2, 1.2)  # Scale the table for readability
# plt.show()

# # Plot graphs for Close and Open prices
# plt.figure(figsize=(10, 6))
# plt.plot(df['date'], df['close'], label='Close Price', color='blue', marker='o')
# plt.plot(df['date'], df['open'], label='Open Price', color='green', marker='x')
# plt.title('Close and Open Prices Over Time')
# plt.xlabel('Date')
# plt.ylabel('Price ($)')
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Plot graphs for High and Low prices
# plt.figure(figsize=(10, 6))
# plt.plot(df['date'], df['high'], label='High Price', color='red', marker='o')
# plt.plot(df['date'], df['low'], label='Low Price', color='orange', marker='x')
# plt.title('High and Low Prices Over Time')
# plt.xlabel('Date')
# plt.ylabel('Price ($)')
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Plot a bar graph for Volume
# plt.figure(figsize=(10, 6))
# plt.bar(df['date'], df['volume'], color='purple')
# plt.title('Volume Over Time')
# plt.xlabel('Date')
# plt.ylabel('Volume')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
