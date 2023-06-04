# import yfinance as yf
# import nsepython as nsp
# # Retrieve stock data using Yahoo Finance API
# # data = yf.download(symbol, start=start_date, end=end_date)
# # if is_nse_stock(symbol):
# #     stock = yf.Ticker(f"{symbol}.NS")
# # else:
# #     stock = yf.Ticker(symbol)
# symbol = "SBIN"
# stock = yf.Ticker(f"{symbol}.NS")
# data = stock.history(period="1mo")

# # Extract the closing prices
# closing_prices = data["Close"][:-1]
# # print(closing_prices)

# # Calculate the daily returns
# daily_returns = closing_prices.pct_change().dropna()
# # print(daily_returns)

# # Calculate the mean and standard deviation of daily returns
# mean_return = daily_returns.mean()

# # Make a simple prediction
# # print(stock.history(period="1d").reset_index().loc[0, 'Open'])
# predicted_price = stock.history(period="1d").reset_index().loc[0, 'Open'] * (1 + mean_return)
# print(predicted_price)
# current_price = stock.history(period="1d").reset_index().loc[0, 'Close']
# print(current_price)

# import model
symbol = "SBIN"
# model = model.PredictModel(f"{symbol}.NS")
# predicted_price = model.get_next_day_pred()
# print(predicted_price)
from nsepython import *
print(nsetools_get_quote(symbol))