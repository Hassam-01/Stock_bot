# Stock Trading Bot

## Overview
This project is a Python-based stock trading bot designed to analyze stock trends, predict market behavior, and recommend actions (BUY, SELL, or HOLD). It uses a combination of statistical evaluations, Markov Decision Processes (MDP), Fuzzy Logic, and Constraint Satisfaction Problems (CSP) to provide actionable insights.

The bot can be run in two modes:
- **Backend Mode:** Connects to the front end via FastAPI using `main.py`.
- **Standalone Mode:** Runs directly in the terminal using `mainLocal.py`.

## Directory Structure

```
.
├── main.py                # Connects to the front end via FastAPI
├── mainLocal.py           # Standalone terminal-based execution
├── utils/                 # Utility scripts for calculations and logic
│   ├── calculations.py    # Statistical evaluations (slope, volatility, RSI, etc.)
│   ├── fetch_data.py      # Fetch historical data from APIs
│   ├── predictions.py     # Implements MDP and fuzzy logic for predictions
│   ├── recommendations.py # CSP-based recommendation system
├── data/                  # Data handling scripts
│   ├── data_extraction.py # Extracts trends and market analysis
├── requirements.txt       # Lists all required Python libraries
```

## Features
- **Calculations:** Perform statistical evaluations like slope, volatility, Relative Strength Index (RSI), and moving average slope.
- **Data Fetching:** Retrieve historical stock data from APIs.
- **Predictions:** Predict market behavior using Markov Decision Processes and fuzzy logic.
- **Recommendations:** Provide actionable recommendations using CSP.
- **Trend Analysis:** Identify five-day-ahead trends and overall market trends.

## Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Usage

### Backend Mode
To run the bot and connect it to the front end (which not required as the project is live):
```bash
py -m uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### Standalone Mode
To run the bot in the terminal:
```bash
py mainLocal.py
```

Follow the prompts to enter the stock symbol, your net worth, and additional information as required.

## Inputs and Outputs
- **Inputs:**
  - Stock symbol (e.g., AAPL, GOOGL).
  - Net worth (required for BUY recommendations).
  - Purchase price and number of stocks owned (required for SELL recommendations).
- **Outputs:**
  - Stock volatility, slope, RSI, moving average slope, and next state.
  - Recommended action: BUY, SELL, or HOLD.

## Technical Details
### Tools and Libraries
- **FastAPI:** Backend framework used in `main.py`.
- **Numpy/Pandas:** For data manipulation and statistical calculations.
- **Matplotlib/Seaborn:** For plotting trends (if needed).

### Core Concepts
- **Markov Decision Processes (MDP):** Predicts future states based on current trends.
- **Fuzzy Logic:** Determines action based on multiple variables like slope, volatility, and RSI.
- **Constraint Satisfaction Problems (CSP):** Recommends actions based on specific constraints and goals.

## Future Enhancements
- Add more robust error handling.
- Integrate additional APIs for more comprehensive data.
- Enhance visualization for trends and predictions.

## Live
Link: https://stock-bot-web-client.vercel.app
