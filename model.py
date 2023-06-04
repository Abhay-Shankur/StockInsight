import yfinance as yf
import nsepython as nse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta


class PredictModel : 
    # Constructor to init and train Model
    def __init__(self, symbol):
        try:
            # Define the stock self.symbol
            self.symbol = symbol

            # Fetch historical stock data from yfinance
            data = yf.download(self.symbol, period="5d", interval='1h')[:-7]
            # print("Data passed to train : ", data, sep="\n")

            # Preprocess the data
            data = data.dropna()  # Remove any rows with missing values

            # Define the features and target variables
            # features = ['Open', 'High', 'Low', 'Close', 'Volume']  # Choose the relevant features from the data
            # features = ['Open', 'Close', 'Volume']  # Choose the relevant features from the data
            self.features = ['Open', 'Close', 'Volume']  # Choose the relevant features from the data
            self.target = 'Close'  # The variable to predict
            # target = ['Close']  # The variable to predict

            # Split the data into training and testing sets
            X = data[self.features]
            y = data[self.target]
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Create and train the model
            self.model = RandomForestRegressor(n_estimators=100)  # You can customize the model as per your requirements
            self.model.fit(self.X_train, self.y_train)

            self.one_month = yf.download(self.symbol, period="1mo")[self.features]
        except Exception() as e:
            print(e)
            

    # Function to get MSE Score for the Model
    def get_mse(self):
        # Make predictions on the testing set
        y_pred = self.model.predict(self.X_test)
        # Evaluate the model's performance
        mse = mean_squared_error(self.y_test, y_pred)
        print("Mean Squared Error:", mse)

    def get_stock_details(self, symbol):
        return nse.nsetools_get_quote(symbol)

    def get_index_details(self, index):
        return nse.nse_get_index_quote(index)

    # 
    def get_next_day_pred(self):
        few_day = yf.download(self.symbol, period="5d")[self.features][:-1]
        next_day_pred = self.model.predict(few_day)
        next_day_pred = next_day_pred.mean()
        print("Predicted : ", next_day_pred)
        print("Actual Price : ", yf.download(self.symbol, period="1d")[self.features], sep="\n")
        return next_day_pred

    # 
    def get_next_6months_pred(self):
        next_six_months = yf.download(self.symbol, period="3mo")[self.features]  
        next_six_months_pred = self.model.predict(next_six_months)
        next_six_months_pred = next_six_months_pred.mean()+(6*self.one_month['Close'].pct_change().mean())
        print("Next Six Months Predictions:", next_six_months_pred)
        return next_six_months_pred

    # 
    def get_next_year_pred(self):
        next_year = yf.download(self.symbol, period="6mo")[self.features]  
        next_year_pred = self.model.predict(next_year)
        next_year_pred = next_year_pred.mean()+(12*self.one_month['Volume'].pct_change().mean())
        print("Next Year Predictions:", next_year_pred)
        return next_year_pred

    # 
    def test_6months(self):
        next_six_months = yf.download(self.symbol, start="2022-01-02", end="2022-05-02")[self.features]  
        # print(next_six_months)
        next_six_months_pred = self.model.predict(next_six_months)
        next_six_months_pred = next_six_months_pred.mean()+(6*self.one_month['Close'].pct_change().mean())
        print("Predicting Price for after 6 months of 2022-05-02 [2022-01-02 | 2022-05-02]")
        print("Next Six Months Predictions:", next_six_months_pred)
        
