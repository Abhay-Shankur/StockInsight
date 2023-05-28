import yfinance as yf
import nsepython as nsp
from flask import Flask, render_template, request, redirect, flash, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key"


def is_nse_stock( symbol):
    list_of_codes = [i for i in nsp.nse_get_advances_declines()['symbol']]
    return symbol in list_of_codes

@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    symbol = request.form.get("symbol")

    try:
        # Retrieve stock data using Yahoo Finance API
        # data = yf.download(symbol, start=start_date, end=end_date)
        if is_nse_stock(symbol):
            stock = yf.Ticker(f"{symbol}.NS")
        else:
            stock = yf.Ticker(symbol)
        data = stock.history(period="1mo")

        # Extract the closing prices
        closing_prices = data["Close"]

        # Calculate the daily returns
        daily_returns = closing_prices.pct_change().dropna()
        # print(daily_returns)

        # Calculate the mean and standard deviation of daily returns
        mean_return = daily_returns.mean()

        # Make a simple prediction
        predicted_price = data.iloc[-1]["Close"] * (1 + mean_return)
        current_price = stock.history(period="1d").reset_index().loc[0, 'Close']
        return jsonify({'message': f'Predicted Stock Price [Close]: {predicted_price} \nCurrent Price: {current_price}', 'type': 'success'})

    except Exception as e:
        # flash(str(e))
        return jsonify({'message': "Invalid Symbol", 'type': 'error'})

@app.route('/marketstatus', methods=["GET"])
def market_status():
    market_status = nsp.nse_marketStatus()['marketState'][0]['marketStatus']
    return jsonify({'market_status': market_status})


if __name__ == "__main__":
    app.run(debug=True)
