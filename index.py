import yfinance as yf
import nsepython as nsp
from flask import Flask, render_template, request, redirect, flash, jsonify
import model

app = Flask(__name__)
# app.secret_key = "your_secret_key"

def is_nse_stock( symbol):
    list_of_codes = [i for i in nsp.nse_get_advances_declines()['symbol']]
    return symbol in list_of_codes

def top_gainers():
    return nsp.nse_get_top_gainers()

def top_losers():
    return nsp.nse_get_top_losers()

def get_index():
    list = []
    for s in nsp.nse_get_index_list()[:4] :
        ns = nsp.nse_get_index_quote(s)
        val1=ns['last'].replace(",","")
        val2=ns['previousClose'].replace(",","")
        res=round(float(val1)-float(val2),2)
        ns['change']=res
        list.append(ns)
    return list

@app.route("/")
def index():
    market_status = nsp.nse_marketStatus()['marketState'][0]['marketStatus']
    return render_template("/index.html", marketstatus=market_status, listgainers=top_gainers(), listlosers=top_losers(), indexes=get_index())


@app.route("/analyze", methods=["POST"])
def analyze():
    symbol = request.form.get("symbol")
    period = request.form.get("period")
    try:
        smodel = model.PredictModel(f"{symbol}.NS")
        if period == "1d":
            predicted_price = smodel.get_next_day_pred()
        elif period == "6m":
            predicted_price = smodel.get_next_6months_pred()
        elif period == "1y":
            predicted_price = smodel.get_next_year_pred()

        return jsonify({'message': f'Predicted Stock Price: {predicted_price}', 'type': 'success'})

    except Exception as e:
        # flash(str(e))
        print(e)
        return jsonify({'message': "Invalid Symbol", 'type': 'error'})

@app.route('/marketstatus', methods=["GET"])
def market_status():
    market_status = nsp.nse_marketStatus()['marketState'][0]['marketStatus']
    return jsonify({'market_status': market_status})

if __name__ == "__main__":
    app.run(debug=False)
