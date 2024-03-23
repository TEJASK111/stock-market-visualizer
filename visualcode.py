#importing python modules 
from matplotlib.pyplot import axis
from menu import menu
import streamlit_antd_components as sac
import streamlit as st 
import pandas as pd  
import yfinance as yf
import datetime  
from datetime import date
from plotly import graph_objs as go
from bs4 import BeautifulSoup
import requests
import time  
import os
import signal
pid = os.getpid()
from streamlit_option_menu import option_menu



#main page setup ,custom header with page icon
st.set_page_config(
    page_title = 'Real-Time stock market ,realtime analysis ',
    page_icon = '✅',
    layout = 'wide',
    initial_sidebar_state="expanded",
)


# header and logo
today = date.today() 
st.write('''# Stock : :blue[The Market Changer]''') 
st.sidebar.image("logo.png", width=250,use_column_width=False)

#side bar section
with st.sidebar: 
        selected = option_menu(
            options=["Stocks Info", "Real-Time Stock data", "sell/buy", 'About', 'exit'],
            icons = ["cast","graph-up-arrow","coin" ,"info-circle","x-octagon"],
            default_index=0,
            menu_title=None,
        )
        
        




#stock info section
if(selected == 'Stocks Info'):
    start = st.sidebar.date_input(
    'Start', datetime.date(2024, 1, 1))
    end = st.sidebar.date_input('End', datetime.date.today())  
    stock_df = pd.read_csv("data.csv")
    st.subheader("STOCK  DATA :book: :pencil:  ", divider='red')
    t = stock_df["Company Name"]
    choice=st.selectbox(r"$\textsf{\Large Enter company name}$" ,t,index=None,placeholder='select company name from dropdown......')
    if choice:
        #imagelink = stock_df[stock_df["Company Name"] == choice]["Image"].values[0]
        #use above line (imagelink) if you want to show the image along with the data (this extract the image from csv through its location,demo is available in data.csv file)
        symbol=stock_df[stock_df["Company Name"] == choice]["Symbol"].values[0]    #extract the symbol from csv file
        data = yf.download(symbol, start=start, end=end)
        data.reset_index(inplace=True)  # reset index
        #st.image(imagelink)   #display the image we extracted throught imagelink   variable
        def plot_line_chart():
            fig = go.Figure()  # create figure
            fig.add_trace(go.Scatter(
                x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
            fig.add_trace(go.Scatter(
                x=data['Date'], y=data['Close'], name="stock_close",line=dict(color='floralwhite')))  # x-axis: date, y-axis: close ,line variable is for the color (can be chnaged as per need)
            fig.layout.update(
                title_text='Line Chart of {}'.format(choice) , xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
            st.plotly_chart(fig)

        def plot_candle_data():  # function for plotting candle data
            fig = go.Figure()  # create figure
            fig.add_trace(go.Candlestick(x=data['Date'],
                                         open=data['Open'],
                                         high=data['High'],  # y-axis: high
                                         low=data['Low'],  # y-axis: low
                                         close=data['Close'], name='market data'))  # y-axis: close
            fig.update_layout(
                title='Candlestick Chart of {}'.format(choice),  # title
                yaxis_title='Stock Price',  # y-axis: title
                xaxis_title='Date')  # x-axis: title
            st.plotly_chart(fig)  # display plotly chart

        chart = (None,'Candle Stick', 'Line Chart')  # chart types
        # dropdown for selecting chart type
        drop1 = st.selectbox(r"$\textsf{\Large Pick your chart}$", chart)
        #r"$\textsf{\Large }$ is used to increase the font size ,streamlit dont have any inbuilt optionto increase font size for st.write and dropdown options
        if st.button("search"):
            st.warning('The symbol of the selected company is: `{}`'.format(symbol))
            if (drop1) == 'Candle Stick':  # if user selects 'Candle Stick'
                plot_candle_data()  # plot candle data
            elif (drop1) == 'Line Chart':  # if user selects 'Line Chart'
                plot_line_chart()  # plot raw data
            else:  # if user doesn't select any chart
                st.write(r"$\textsf{\Large please select a graph type}$")  # plot candle data
            st.subheader('Raw Data of {}'.format(choice))
            st.write(data)   
    else:
        st.write(r"$\textsf{\Large Please select a option from dropdown}$")
    



#real time stock data section , if market is closed at current time there will be no data shown to you
elif(selected == 'Real-Time Stock data'):  # if user selects 'Real-Time Stock Price'
    stock_df = pd.read_csv("data.csv")
    st.subheader("REAL TIME VISUALIZATION OF STOCK PRICE :chart_with_downwards_trend: :bar_chart: :chart_with_upwards_trend: ", divider='red')
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    option = st.selectbox(r"$\textsf{\Large Please select a company}$",tickers,index=None,placeholder='select company name from dropdown......')
    if option:
        symbol=stock_df[stock_df["Company Name"] == option]["Symbol"].values[0]
        if st.button("SEARCH"):
            #web stuff starts from here aka Web scraping 
            btc_url = 'https://finance.yahoo.com/quote/'+symbol
            headers = {'User-agent': 'Mozilla/5.0'}   #do include this line else the data wont be shown to you
            placeholder = st.empty()        
            while True:
                btc_page = requests.get(btc_url, headers=headers)
                btc_soup = BeautifulSoup(btc_page.content, 'html.parser')
                btc_price= btc_soup.find('fin-streamer', {'data-symbol':{symbol}, 'data-field':'regularMarketPrice'}).text
                btc_change = btc_soup.find('fin-streamer', {'data-symbol':{symbol}, 'data-field':'regularMarketChange'}).text
                btc_changeper = btc_soup.find('fin-streamer', {'data-symbol': {symbol},'data-field':'regularMarketChangePercent'}).text
                change_delta = f"{btc_change} {btc_changeper}"
                current_date = datetime.datetime.now()
                tomorrow_date = current_date + datetime.timedelta(days=1)
                start_date = current_date.strftime("%Y-%m-%d")
                end_date = tomorrow_date.strftime("%Y-%m-%d")
                data=yf.download(symbol, start=start_date, end=end_date, interval="1m")  #shows data between today and tomorrow , so only today data will be shon if market is currently working
                with placeholder.container():
                    st.metric(label=symbol, value= btc_price , delta=change_delta)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], name='Adjusted Close'))
                    fig.update_layout(title='Adjusted Close Prices for {}'.format(symbol),
                                      xaxis_title='Date',
                                      yaxis_title='Price')
                    st.plotly_chart(fig)  
                time.sleep(2)                  
    else:
        st.write(r"$\textsf{\Large please select a option to continue}$ ")



# stock market simulator section starts from here
elif(selected == 'sell/buy'): 
    st.subheader("(simulator) Stock Market :dart:  :black_joker: :slot_machine:  ",divider='blue')
    if "resp" not in st.session_state:
       st.session_state.resp = None
    st.session_state._resp = st.session_state.resp
    def resp_set():
        st.session_state.resp = st.session_state._resp
    choice=st.selectbox(r"$\textsf{\Large Do you want to invest in stock market (simulator)}$",[None,'Yes','No'],key="_resp",placeholder='select option from dropdown', on_change=resp_set)
    menu()
    if choice=='Yes':
        st.warning(" Now you can head over to '(simulator)stock market' option from sidebar menu , by scrolling  down")
    else :
        if choice=='No':
            st.warning("you can choose other options from sidebar")
        else:
            st.write("please select a option from dropdown")

    sac.alert(label='Stock market timing alert', description='The NSE/BSE closes at 3:30pm and remains closed on weekends', banner=True, icon=True, closable=False)  



#about section
elif(selected == 'About'): 
    st.subheader("ABOUT THE PROJECT   👾 ℹ️ ", divider='green')
    st.error("this app is made with python using streamlit (a web server based python library), as a backend to help us run it on the web server. this app is also hosted on the app under this link ""https://stock-market-visualizer.streamlit.app/" )   




#exit section, streamlit has 'ctrl+c' break issue ,so this will help you to close this application 
elif(selected == 'exit'): 
    st.subheader("EXIT ❎ ", divider='violet')
    st.error("The server has stopped. Please close the  browser window.")
    time.sleep(3)
    # Send SIGTERM signal to stop the Streamlit server
    os.kill(pid, signal.SIGTERM)



#end
