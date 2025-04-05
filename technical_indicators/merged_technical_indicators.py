# change base_path below to match your pc path

# import necessary dependencies
import pandas as pd
import os

companies = ['AAPL', 'GOOG', 'AMZN', 'MSFT', 'META', 'NVDA']
indicators = [
    ('SMA', 'sma'),
    ('ADX', 'adx'),
    ('DEMA', 'dema'),
    ('EMA', 'ema'),
    ('RSI', 'rsi'),
    ('STANDARDDEVIATION', 'standardDeviation'),
    ('TEMA', 'tema'),
    ('WILLIAMS', 'williams'),
    ('WMA', 'wma')
]

# change base_path to match your pc path
base_path = '/Users/sarithakumarik/Documents/DATA6300/Data/technical_indicators/'

def merge_company_data(symbol):
    merged_df = None

    for folder, indicator in indicators:
        file_path = f'{base_path}{folder}/{symbol}_{indicator}_Daily.csv'
        
        try:
            df = pd.read_csv(file_path)
            df = df[['date', indicator]]
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on='date', how='left')        
        except FileNotFoundError:
            print(f"Warning: File not found for {symbol} in {folder}. Skipping this indicator.")

    if merged_df is not None:
        merged_df['symbol'] = symbol
        merged_df['date'] = pd.to_datetime(merged_df['date'], format='%d-%m-%Y')
        merged_df = merged_df.sort_values(by='date', ascending=True)
        columns = ['date', 'symbol'] + [col for col in merged_df.columns if col not in ['date', 'symbol']]
        merged_df = merged_df[columns]
        merged_df['date'] = merged_df['date'].dt.strftime('%d-%m-%Y')

        output_dir = f'{base_path}Merged_Technical_Indicators'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f'{output_dir}/{symbol}_Technical_Indicators.csv'
        merged_df.to_csv(output_file, index=False)
        print(f'Merged data for {symbol} saved to {output_file}')
    else:
        print(f"No data to merge for {symbol}.")


for company in companies:
    merge_company_data(company)
