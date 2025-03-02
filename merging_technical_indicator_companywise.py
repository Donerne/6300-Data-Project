import pandas as pd

companies = ['AAPL', 'GOOG', 'AMZN', 'MSFT', 'META', 'NVDA']

base_path = '/Users/sarithakumarik/Documents/DATA6300/Data/'

def merge_company_data(symbol):
    sma_file = f'{base_path}SMA/{symbol}_SMA_Daily.csv'
    adx_file = f'{base_path}ADX/{symbol}_ADX_Daily.csv'
    dema_file = f'{base_path}DEMA/{symbol}_DEMA_Daily.csv'
    ema_file = f'{base_path}EMA/{symbol}_EMA_Daily.csv'
    rsi_file = f'{base_path}RSI/{symbol}_RSI_Daily.csv'
    std_dev_file = f'{base_path}STD_DEV/{symbol}_STD_DEV_Daily.csv'
    tema_file = f'{base_path}TEMA/{symbol}_TEMA_Daily.csv'
    williams_file = f'{base_path}WILLIAM/{symbol}_WILLIAM_Daily.csv'
    wma_file = f'{base_path}WMA/{symbol}_WMA_Daily.csv'

    sma_df = pd.read_csv(sma_file)
    adx_df = pd.read_csv(adx_file)
    dema_df = pd.read_csv(dema_file)
    ema_df = pd.read_csv(ema_file)
    rsi_df = pd.read_csv(rsi_file)
    std_dev_df = pd.read_csv(std_dev_file)
    tema_df = pd.read_csv(tema_file)
    williams_df = pd.read_csv(williams_file)
    wma_df = pd.read_csv(wma_file)

    merged_df = sma_df
    merged_df = pd.merge(merged_df, adx_df[['date', 'adx']], on='date', how='left')
    merged_df = pd.merge(merged_df, dema_df[['date', 'dema']], on='date', how='left')
    merged_df = pd.merge(merged_df, ema_df[['date', 'ema']], on='date', how='left')
    merged_df = pd.merge(merged_df, rsi_df[['date', 'rsi']], on='date', how='left')
    merged_df = pd.merge(merged_df, std_dev_df[['date', 'standardDeviation']], on='date', how='left')
    merged_df = pd.merge(merged_df, tema_df[['date', 'tema']], on='date', how='left')
    merged_df = pd.merge(merged_df, williams_df[['date', 'williams']], on='date', how='left')
    merged_df = pd.merge(merged_df, wma_df[['date', 'wma']], on='date', how='left')
    merged_df['symbol'] = symbol

    columns = ['date', 'symbol'] + [col for col in merged_df.columns if col not in ['date', 'symbol']]
    merged_df = merged_df[columns]

    output_file = f'{base_path}Merged_Technical_Indicators/{symbol}_Technical_Indicators.csv'
    merged_df.to_csv(output_file, index=False)
    print(f'Merged data for {symbol} saved to {output_file}')

for company in companies:
    merge_company_data(company)
