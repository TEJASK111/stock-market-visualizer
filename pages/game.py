import streamlit as st
import os
from menu import menu_with_redirect
import yfinance as yf
import time, sys
import pandas as pd 
import datetime 
import streamlit_shadcn_ui as ui
from plotly import graph_objs as go 

menu_with_redirect()


# Verify the user's response
if st.session_state.resp not in ["Yes"]:
    st.warning("You do not have permission to view this page.")
    st.stop()
#balance file option
if os.path.exists("balance.txt"):
    with open("balance.txt", "r") as f:
        balance = float(f.read())
else:
    balance = 10000
    with open("balance.txt", "w") as f:
        f.write(str(balance))

stock_df = pd.read_csv('data.csv')
d = stock_df["Company Name"]
kp1,fig1 = st.columns(2)   #making 2 columns  for dropdown and chart
option = kp1.selectbox(r"$\textsf{\Large Pick the company, whose stock you want to buy}$", d, index=None, placeholder='select name from dropdown...')  # for single select from list
chart_type=fig1.selectbox(r"$\textsf{\Large Pick the chart type of your need}$",[None,'line','candle'])
st.write(r"$\textsf{\Large You have 10000 INR as balance}$")
if option:
    symbol = stock_df[stock_df["Company Name"] == option]["Symbol"].values[0]
    now = datetime.datetime.now()
    stock_data = yf.Ticker(symbol)
    current_price = stock_data.info['currentPrice']
    st.write("the current price of stock is :", current_price)
    start = (now - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    def plot_raw_data():  # function for plotting raw data
        fig = go.Figure()  # create figure
        fig.add_trace(go.Scatter(  # add scatter plot
            x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
        fig.add_trace(go.Scatter(  # add scatter plot
            x=data['Date'], y=data['Close'], name="stock_close",line=dict(color='floralwhite')))  # x-axis: date, y-axis: close
        fig.layout.update(  # update layout
            title_text='Line Chart of {}'.format(option) , xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
        st.plotly_chart(fig)  # display plotly chart
    def plot_candle_data():  # function for plotting candle data
        fig = go.Figure()  # create figure
        fig.add_trace(go.Candlestick(x=data['Date'],  # add candlestick plot
                                     open=data['Open'],
                                     high=data['High'],  # y-axis: high
                                     low=data['Low'],  # y-axis: low
                                     close=data['Close'], name='market data'))  # y-axis: close
        fig.update_layout(  # update layout
            title='Candlestick Chart of {}'.format(option),  # title
            yaxis_title='Stock Price',  # y-axis: title
            xaxis_title='Date')  # x-axis: title
        st.plotly_chart(fig)  # display plotly chart
    if (chart_type) == 'candle':
        plot_candle_data()  # plot candle data
    else :  # if user selects 'Line Chart'
        plot_raw_data()  # plot raw data
    x = st.slider("choose value between 1-10", min_value=1, max_value=10, step=1)  #slider
    st.write("the stock amount is :", x, "shares price is",current_price*x )
    if st.button("Buy"):
        used_money=x*current_price
        if (used_money<balance):
            balance=balance-used_money
            st.write("you brought ",x,"stocks from",option,"company and now you have",balance,"INR left to use")
            #the stock data is saved in stockdata.csv file
            if not os.path.exists("stockdata.csv"):
                with open("stockdata.csv","w") as f:
                    f.write("Symbol,amount\n")
            with open("stockdata.csv",'a') as f:
                f.write(f"{symbol},{x}\n")
            with open("balance.txt","w") as f:
                f.write(str(balance))
        else:
            st.write("you cant buy  stocks,check balance")
            
    if st.button("sell"):
        da=pd.read_csv("stockdata.csv")
        total_value = 0
    
        for index, row in da.iterrows():
            symbol = row["Symbol"]
            amount = row["amount"]
            stock_price = yf.Ticker(symbol).info['currentPrice']
            total_value += amount * stock_price
        st.warning("the total value of sold stock is :"+str(total_value))
        st.error("now you can go back to main ,by clicking on 'go back to main' button from side bar")
        #deleting file ,so next time the when user start the new entry the data dont get mixed up
        file_path = "balance.txt"
        if os.path.isfile(file_path):
            os.remove(file_path)
        file_path2='stockdata.csv'
        if os.path.isfile(file_path2):
            os.remove(file_path2)
    #below was a attempt tomake a popup and i failed in it 
    #trigger_btn = ui.button(text="Display Result", key="trigger_btn_1")
    #ui.alert_dialog(show=trigger_btn, title="STOCK PROFIT", description=" The total value of stocks is :".format(total_value), confirm_label="OK", cancel_label="Cancel", key="alert_dialog_1")
else:
    st.write(r"$\textsf{\Large Please select a option}$")
    
    #end
