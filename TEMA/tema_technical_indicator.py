import requests
import pandas as pd
import os
from datetime import datetime, timedelta

api_key = "DfrdNtpDtF8RSp1gnBd0auOJ0562NslK"

stocks = [
    {"symbol": "AMZN", "ipo_date": "1997-05-15"},
    {"symbol": "AAPL", "ipo_date": "1980-12-12"},
    {"symbol": "GOOG", "ipo_date": "2004-08-19"},
    {"symbol": "MSFT", "ipo_date": "1986-03-13"},
    {"symbol": "META", "ipo_date": "2012-05-18"},
    {"symbol": "NVDA", "ipo_date": "1999-01-22"}
]

def format_date_api(date):
    return date.strftime("%Y-%m-%d")

def format_date_output(date):
    return date.strftime("%d-%m-%Y")

for stock in stocks:
    symbol = stock["symbol"]
    ipo_date = datetime.strptime(stock["ipo_date"], "%Y-%m-%d")
    start_date = datetime.today()
    all_data = []
    
    while start_date > ipo_date:
        to_date = format_date_api(start_date)
        from_date = start_date - timedelta(days=4*365)

        if from_date < ipo_date:
            from_date = ipo_date      
        from_date_str = format_date_api(from_date)
        
        url = f"https://financialmodelingprep.com/api/v3/technical_indicator/daily/{symbol}?type=tema&period=1day&apikey={api_key}&from={from_date_str}&to={to_date}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()            
            if data:
                df = pd.DataFrame(data)                
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')                
                df['symbol'] = symbol
                all_data.append(df)                
                print(f"Data fetched for {symbol} from {format_date_output(from_date)} to {format_date_output(start_date)}")
            else:
                print(f"No data available for {symbol} from {format_date_output(from_date)} to {format_date_output(start_date)}")
        else:
            print(f"Failed to fetch data for {symbol} from {format_date_output(from_date)} to {format_date_output(start_date)}. Status code: {response.status_code}")
        start_date = from_date

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.drop_duplicates(subset=['date', 'symbol'], keep='first', inplace=True)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(current_directory, f"{symbol}_TEMA_Daily.csv")
        final_df.to_csv(file_name, index=False)        
        print(f"Final data saved for {symbol} to {file_name}")
