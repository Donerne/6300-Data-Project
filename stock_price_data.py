import requests
import csv
from datetime import datetime

# Define the stock details (symbol, IPO date)
stocks = [
    {"symbol": "AMZN", "ipo_date": "1997-05-15"},
    {"symbol": "AAPL", "ipo_date": "1980-12-12"},
    {"symbol": "GOOG", "ipo_date": "2004-08-19"},
    {"symbol": "MSFT", "ipo_date": "1986-03-13"},
    {"symbol": "META", "ipo_date": "2012-05-18"},
    {"symbol": "NVDA", "ipo_date": "1999-01-22"}

    # We also pulled the data for month of March 2025 which we forecasted to compare, evaluate and perform correlations
    # {"symbol": "AMZN", "ipo_date": "2025-03-05"},
    # {"symbol": "AAPL", "ipo_date": "2025-03-05"},
    # {"symbol": "GOOG", "ipo_date": "2025-03-05"},
    # {"symbol": "MSFT", "ipo_date": "2025-03-05"},
    # {"symbol": "META", "ipo_date": "2025-03-05"},
    # {"symbol": "NVDA", "ipo_date": "2025-03-05"}
]


# Defining the API token (you can use either token. We are using the free version so when one token limit runs out, use the other.)
# token = "4ccd7cc6c674d64e9055f9ce81f362c4543707c0"
token = "974d47176476fe62f2640d26bae719cec1e134e6"

# Loop through each stock symbol and fetch its data
for stock in stocks:
    # Construct the URL for each stock's historical data
    url = f"https://api.tiingo.com/tiingo/daily/{stock['symbol']}/prices?startDate={stock['ipo_date']}&token={token}"
    
    # url = f"https://api.tiingo.com/tiingo/daily/{stock['symbol']}/prices?startDate={stock['ipo_date']}&endDate='2025-03-25'&token={token}"
    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        data = response.json()
        # csv_file = f"march_prices/{stock['symbol']}_march_prices.csv"
        csv_file = f"Stock_Price_Data/{stock['symbol']}_stock_prices.csv"
        formatted_data = []

        if data:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = None

                for record in data:
                    if 'date' in record:

                        date_str = datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%Y')

                    try:
                        formatted_data.append({
                        "date": date_str,
                        f"{stock['symbol']}_close": record.get("close", ""),
                        f"{stock['symbol']}_high": record.get("high", ""),
                        f"{stock['symbol']}_low": record.get("low", ""),
                        f"{stock['symbol']}_open": record.get("open", ""),
                        f"{stock['symbol']}_traded_volume": record.get("volume", ""),
                        f"{stock['symbol']}_adjClose": record.get("adjClose", ""),
                        f"{stock['symbol']}_adjLow": record.get("adjLow", ""),
                        f"{stock['symbol']}_adjOpen": record.get("adjOpen", ""),
                        f"{stock['symbol']}_adj_traded_volume": record.get("adjVolume", ""),
                        f"{stock['symbol']}_divCash": record.get("divCash", ""),
                        f"{stock['symbol']}_splitFactor": record.get("splitFactor", ""),
                        })

                    except ValueError as e:
                        print(f"Error processing date {record['date']}: {e}")
                        
                keys = formatted_data[0].keys()
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(formatted_data)

            print(f"Data for {stock['symbol']} written to {csv_file}")
        else:
            print(f"No data found for {stock['symbol']}.")

    else:
        print(f"Failed to fetch data for {stock['symbol']}. HTTP Status Code: {response.status_code}")

print("All stock data successfully written to their respective CSV files.")