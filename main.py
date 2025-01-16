import requests
from twilio.rest import Client
import pandas as pd
import numpy as np
from datetime import date, timedelta



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"


## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").





stock_params = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'outputsize': "compact",
    'apikey': stock_api_key,
    'datatype': 'csv'
}

current_date =date.today()
days_to_subtract = 3
last_7_days = current_date - timedelta(days=days_to_subtract)

news_params = {
    
    'qInTitle': "tesla",
    'from': last_7_days,
    'to': current_date,
    'language': 'en',
    'sortBy': 'relevancy'
}


# API calls
stock_data_response = requests.get(STOCK_ENDPOINT, params=stock_params)
news_data_response = requests.get(NEWS_ENDPOINT, params=news_params)

stock_data_response.raise_for_status()
news_data_response.raise_for_status()


article_list = []

for article in news_data_response.json()['articles']:
    article_details = (f"Headline: {article['title']}\nBrief: {article['description']}\nURL: {article['url']}")
    article_list.append(article_details)


# writing stock data to csv file
with open('Tesla_stock_data.csv', 'wb') as f:
    f.write(stock_data_response.content)


# loading into a pandas dataframe
stock_data = pd.read_csv('Tesla_stock_data.csv')

print(stock_data)

# obtaining yesterday and day before yesterday price values
yesterday_price = stock_data.loc[0, 'close']
day_before_yesterday_price = stock_data.loc[1, 'close']


print(yesterday_price)
print(day_before_yesterday_price)


stock_price_difference = yesterday_price - day_before_yesterday_price
print(stock_price_difference)


percent_diff = round((stock_price_difference / day_before_yesterday_price) * 100, 3)
print(percent_diff,"%")

top_3_articles = article_list[:3]
print("\n".join(top_3_articles))


# if percent_diff > 5:
#     print("\n".join(top_3_articles))
# else:
#     print(f"No action required, percentage change: {percent_diff}")
#     ## STEP 2: https://newsapi.org/ 

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation 


for news in top_3_articles:
    client = Client(account_sid, auth_token)

    if stock_price_difference > 0:
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=f"TSLA: 🔺{abs(percent_diff)}% \n {news}",
            # from_='+17753207011',
            to="whatsapp:+16473939783")

        print(message.status)
    else:
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=f"TSLA: 🔻{abs(percent_diff)}% \n {news}",
            # from_='+17753207011',
            to="whatsapp:+16473939783")

        print(message.status)


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

