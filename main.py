import requests
import pandas as pd
import numpy as np
from datetime import date, timedelta
import csv


STOCK_NAME = "AAPL"
COMPANY_NAME = "Apple Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"


# #TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = "AC8c2513d7bf6da54ede23693275344658"
# auth_token = "10fafd5ea276e691fa3c0154bcfd27e7"

# Setting up APIs
stock_api_key = "0WHYEF2HDYMWM313"
# news_api_key = "1b3b397afaa34a7b8f1589a45af74273"


stock_params = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'outputsize': "compact",
    'apikey': stock_api_key,
    'datatype': 'csv'
}

current_date =date.today()
days_to_subtract = 30
last_30_days = current_date - timedelta(days=days_to_subtract)

# news_params = {
#     'apiKey': "1b3b397afaa34a7b8f1589a45af74273",
#     'qInTitle': "nvidia",
#     'from': last_30_days,
#     'to': current_date,
#     'language': 'en',
#     'sortBy': 'relevancy'
# }


# API calls
stock_data_response = requests.get(STOCK_ENDPOINT, params=stock_params)
# news_data_response = requests.get(NEWS_ENDPOINT, params=news_params)

stock_data_response.raise_for_status()
# news_data_response.raise_for_status()


# article_list = []

# for article in news_data_response.json()['articles']:
#     article_details = (f"Headline: {article['title']}\nBrief: {article['description']}\nURL: {article['url']}\nDATE: {article['publishedAt']}")
#     article_list.append(article_details)


# # writing stock data to csv file
# with open('Tesla_stock_data.csv', 'wb') as f:
#     f.write(stock_data_response.content)


# loading into a pandas dataframe
# stock_data = pd.read_csv('Tesla_stock_data.csv')

print(stock_data_response.content)

# # obtaining yesterday and day before yesterday price values
# yesterday_price = stock_data.loc[0, 'close']
# day_before_yesterday_price = stock_data.loc[1, 'close']


# print(yesterday_price)
# print(day_before_yesterday_price)


# stock_price_difference = yesterday_price - day_before_yesterday_price
# print(stock_price_difference)


# percent_diff = round((stock_price_difference / day_before_yesterday_price) * 100, 3)
# print(percent_diff,"%")

# top_articles = article_list
# print("\n".join(top_articles))


# if percent_diff > 5:
#     print("\n".join(top_3_articles))
# else:
#     print(f"No action required, percentage change: {percent_diff}")
#     ## STEP 2: https://newsapi.org/ 



# for news in top_3_articles:
#     client = Client(account_sid, auth_token)

#     if stock_price_difference > 0:
#         message = client.messages.create(
#             from_="whatsapp:+14155238886",
#             body=f"TSLA: 🔺{abs(percent_diff)}% \n {news}",
#             # from_='+17753207011',
#             to="whatsapp:+16473939783")

#         print(message.status)
#     else:
#         message = client.messages.create(
#             from_="whatsapp:+14155238886",
#             body=f"TSLA: 🔻{abs(percent_diff)}% \n {news}",
#             # from_='+17753207011',
#             to="whatsapp:+16473939783")

#         print(message.status)

