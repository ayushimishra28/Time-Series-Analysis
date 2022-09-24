import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
import pandas_ta as pta
import dateutil
st.set_page_config(
        page_title="Stock Analysis",
        page_icon="page_with_curl",
        layout="wide",
    )

st.title("Stock Anaysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock Ticker', 'TSLA')
with col2:
    star_date = st.date_input("Start Date", datetime.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input("End Date", datetime.date(today.year,today.month,today.day))

def plotly_table(dataframe):
        headerColor = 'grey'
        rowEvenColor = '#f8fafd'
        rowOddColor = '#e1efff'
        fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
            line_color='#0078ff', fill_color='#0078ff',
            align='center', font=dict(color='white', size=15),height =35,
        ),
        cells=dict(
            values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns], fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*10],
            align='left', line_color=['white'],font=dict(color=["black"], size=15)
        ))
        ])
        fig.update_layout( height= 400, margin=dict(l=0, r=0, t=0, b=0))
        return fig

data = yf.download(ticker, start=star_date, end=end_date)

if len(data) <1:
    st.write('##### Please write the name of valid Ticker')
else:
    
    data.index = [str(i)[:10] for i in data.index]
    fig_tail = plotly_table(data.tail(10).sort_index(ascending = False).round(3))
    fig_tail.update_layout(height = 220)
    st.write('##### Historical Data (Last 10 days)')
    st.plotly_chart(fig_tail, use_container_width=True)

    def filter_data(dataframe, num_period):
        if num_period == '1mo':
            date = data1.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
        elif num_period == '5d':
            date = data1.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
        elif num_period == '6mo':
            date = data1.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
        elif num_period == '1y':
            date = data1.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
        elif num_period == '5y':
            date = data1.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
        elif num_period == 'ytd':
            date = datetime.datetime(data1.index[-1].year, 1,1).strftime('%Y-%m-%d')
        else:
            date = dataframe.index[0]
        
        return dataframe.reset_index()[dataframe.reset_index()['Date']>date]

    def close_chart(dataframe, num_period):
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                            mode='lines',
                            name='Open',line = dict( width=2,color = '#5ab7ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                            mode='lines',
                            name='Close',line = dict( width=2,color = 'black')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                            mode='lines', name='High',line = dict( width=2,color = '#0078ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                            mode='lines', name='Low',line = dict( width=2,color = 'red')))
        fig.add_trace(go.Bar(name='Volume (in millions)', x=dataframe['Date'], y=dataframe['Volume']/1000000,marker_color='#79da84',  marker_line=dict(width=0.2, color='#0078ff')))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend=dict(
        yanchor="top",
        xanchor="right"
        ))
        return fig

    def candlestick(dataframe, num_period):
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=dataframe['Date'],
                        open=dataframe['Open'], high=dataframe['High'],
                        low=dataframe['Low'], close=dataframe['Close']))

        fig.add_trace(go.Bar(name='Volume (in millions)', x=dataframe['Date'],y=dataframe['Volume']/1000000,marker_color='#79da84',  marker_line=dict(width=0.2, color='#0078ff')))
        fig.update_layout(showlegend = False,height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white', paper_bgcolor = '#e1efff')
        return fig

    

    def RSI(dataframe, num_period):
        dataframe['RSI'] = pta.rsi(dataframe['Close'])
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dataframe['Date'],
            y=dataframe.RSI, name = 'RSI',marker_color='orange',line = dict( width=2,color = 'orange'),
        ))
        fig.add_trace(go.Scatter(

            x=dataframe['Date'],
            y=[70]*len(dataframe), name = 'Overbought', marker_color='red',line = dict( width=2,color = 'red',dash='dash'),
        ))

        fig.add_trace(go.Scatter(
            x=dataframe['Date'],
            y=[30]*len(dataframe),fill='tonexty', name = 'Oversold', marker_color='#79da84',line = dict( width=2,color = '#79da84',dash='dash'),
        ))

        fig.update_layout(yaxis_range=[0,100],
            height=200,plot_bgcolor = 'white', paper_bgcolor = '#e1efff',margin=dict(l=0, r=0, t=0, b=0),legend=dict(orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1
        )
        )
        return fig

    

    def Moving_average(dataframe,num_period):
        
        dataframe['SMA_50'] = pta.sma(dataframe['Close'],50) 
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                            mode='lines',
                            name='Open',line = dict( width=2,color = '#5ab7ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                            mode='lines',
                            name='Close',line = dict( width=2,color = 'black')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                            mode='lines', name='High',line = dict( width=2,color = '#0078ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                            mode='lines', name='Low',line = dict( width=2,color = 'red')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                            mode='lines', name='SMA 50',line = dict( width=2,color = 'purple')))
        fig.add_trace(go.Bar(name='Volume (in millions)', x=dataframe['Date'], y=dataframe['Volume']/1000000,marker_color='#79da84',  marker_line=dict(width=0.2, color='#0078ff')))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend=dict(
        yanchor="top",
        xanchor="right"
        ))
        
        return fig
    def Moving_average_candle_stick(dataframe,num_period):
    
        dataframe['SMA_50'] = pta.sma(dataframe['Close'],50) 
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=dataframe.index,
                        open=dataframe['Open'], high=dataframe['High'],
                        low=dataframe['Low'], close=dataframe['Close']))
    
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                            mode='lines', name='SMA 50',line = dict( width=2,color = 'purple')))
        fig.add_trace(go.Bar(name='Volume (in millions)', x=dataframe.index, y=dataframe['Volume']/1000000,marker_color='#79da84',  marker_line=dict(width=0.2, color='#0078ff')))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend=dict(
        yanchor="top",
        xanchor="right"
        ))
        
        return fig

    def MACD(dataframe, num_period):
        macd = pta.macd(dataframe['Close']).iloc[:,0]
        macd_signal = pta.macd(dataframe['Close']).iloc[:,1]
        macd_hist = pta.macd(dataframe['Close']).iloc[:,2]
        dataframe['MACD'] = macd
        dataframe['MACD Signal'] = macd_signal
        dataframe['MACD Hist'] = macd_hist
        dataframe = filter_data(dataframe,num_period)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dataframe['Date'],
            y=dataframe['MACD'], name = 'RSI',marker_color='orange',line = dict( width=2,color = 'orange'),
        ))
        fig.add_trace(go.Scatter(

            x=dataframe['Date'],
            y=dataframe['MACD Signal'], name = 'Overbought', marker_color='red',line = dict( width=2,color = 'red',dash='dash'),
        ))
        c = ['red' if cl <0 else "green" for cl in macd_hist]
        fig.add_trace(go.Bar(name='Volume (in millions)', x=dataframe['Date'], y=dataframe['MACD Hist'],marker_color=c,  marker_line=dict(width=0.2, color='#0078ff')))
        

        fig.update_layout(
            height=200,plot_bgcolor = 'white', paper_bgcolor = '#e1efff',margin=dict(l=0, r=0, t=0, b=0),legend=dict(orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1
        )
        )
        return fig
    
   
    st.markdown("""<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #e1efff;
            color:black;
        }
        div.stButton > button:hover {
            background-color: #0078ff;
            color:white;
            }
        </style>""", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11,col12,col13,col14,col15,col16,col17 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

    num_period = ''
    with col1:
        if st.button('5D'):
            num_period = '5d'
    with col2:
        if st.button('1M'):
            num_period = '1mo'
    with col3:
        if st.button('6M'):
            num_period = '6mo'
    with col4:
        if st.button('YTD'):
            num_period = 'ytd'
    with col5:
        if st.button('1Y'):
            num_period = '1y'
    with col6:
        if st.button('5Y'):
            num_period = '5y'
    with col7:
        if st.button('MAX'):
            num_period = 'max'
    
    col1, col2, col3 = st.columns([1,1,4])
    with col1:
        chart_type = st.selectbox('',('Candle','Line'))
    with col2:
        indicators = st.selectbox('',('RSI', 'Moving Average','MACD'))

    ticker_ = yf.Ticker(ticker)
    new_df1 = ticker_.history(period = 'max')
    data1 = ticker_.history(period = 'max')
    if num_period == '':

        if chart_type == 'Candle' and indicators == 'RSI':
            st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
            st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

        if chart_type == 'Candle' and indicators == 'Moving Average':
            st.plotly_chart(Moving_average_candle_stick(data1, '1y'), use_container_width=True)

        if chart_type == 'Candle' and indicators == 'MACD':
            st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
            st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

        if chart_type == 'Line' and indicators == 'RSI':
            st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
            st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

        if chart_type == 'Line' and indicators == 'Moving Average':
            st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

        if chart_type == 'Line' and indicators == 'MACD':
            st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
            st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

     

    else:

        if chart_type == 'Candle' and indicators == 'RSI':
            st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
            st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

        if chart_type == 'Candle' and indicators == 'Moving Average':
            st.plotly_chart(Moving_average_candle_stick(new_df1, num_period), use_container_width=True)

        if chart_type == 'Candle' and indicators == 'MACD':
            st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
            st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

        if chart_type == 'Line' and indicators == 'RSI':
            st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
            st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

        if chart_type == 'Line' and indicators == 'Moving Average':
            st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)
        if chart_type == 'Line' and indicators == 'MACD':
            st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
            st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
