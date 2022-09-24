import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import sys

st.set_page_config(
        page_title="Comparing Stocks",
        page_icon="bar_chart",
        layout="wide",
    )

st.title("Comparing Stocks ")
try:
    
    options = st.multiselect('Select up to 4 stocks',
        ['SBIN.NS', 'IBN', 'HDFCBANK.NS', 'KOTAKBANK.NS','TCS','INFY','WIT'],
        ['SBIN.NS', 'IBN', 'HDFCBANK.NS', 'KOTAKBANK.NS'])

    stock1 = yf.Ticker(options[0])
    stock2 = yf.Ticker(options[1])
    stock3 = yf.Ticker(options[2])
    stock4 = yf.Ticker(options[3])

    df1 = stock1.history(period = '6mo')
    df2 = stock2.history(period = '6mo')
    df3 = stock3.history(period = '6mo')
    df4 = stock4.history(period = '6mo')

    BS1 = stock1.balancesheet.iloc[:,::-1]
    BS2 = stock2.balancesheet.iloc[:,::-1]
    BS3 = stock3.balancesheet.iloc[:,::-1]
    BS4 = stock4.balancesheet.iloc[:,::-1]

    IC1 = stock1.financials
    IC2 = stock2.financials
    IC3 = stock3.financials
    IC4 = stock4.financials

    CR1 = BS1.loc['Total Current Assets'].astype(float) / BS1.loc['Total Current Liabilities'].astype(float) 
    CR2 = BS2.loc['Total Current Assets'].astype(float) / BS2.loc['Total Current Liabilities'].astype(float) 
    CR3 = BS3.loc['Total Current Assets'].astype(float) / BS3.loc['Total Current Liabilities'].astype(float) 
    CR4 = BS4.loc['Total Current Assets'].astype(float) / BS4.loc['Total Current Liabilities'].astype(float) 

    TAT1 = IC1.loc['Total Revenue'].astype(float)/BS1.loc['Total Assets'].astype(float)
    TAT2 = IC2.loc['Total Revenue'].astype(float)/BS2.loc['Total Assets'].astype(float)
    TAT3 = IC3.loc['Total Revenue'].astype(float)/BS3.loc['Total Assets'].astype(float)
    TAT4 = IC4.loc['Total Revenue'].astype(float)/BS4.loc['Total Assets'].astype(float)

    TDR1 = BS1.loc['Total Liab'].astype(float) / BS1.loc['Total Assets'].astype(float)
    TDR2 = BS2.loc['Total Liab'].astype(float) / BS2.loc['Total Assets'].astype(float)
    TDR3 = BS3.loc['Total Liab'].astype(float) / BS3.loc['Total Assets'].astype(float)
    TDR4 = BS4.loc['Total Liab'].astype(float) / BS4.loc['Total Assets'].astype(float)

    DE1 = BS1.loc['Total Liab'].astype(float) / BS1.loc["Total Stockholder Equity"].astype(float)
    DE2 = BS2.loc['Total Liab'].astype(float) / BS2.loc["Total Stockholder Equity"].astype(float)
    DE3 = BS3.loc['Total Liab'].astype(float) / BS3.loc["Total Stockholder Equity"].astype(float)
    DE4 = BS4.loc['Total Liab'].astype(float) / BS4.loc["Total Stockholder Equity"].astype(float)

    ER1 = BS1.loc["Total Stockholder Equity"].astype(float) / BS1.loc['Total Assets'].astype(float) 
    ER2 = BS2.loc["Total Stockholder Equity"].astype(float) / BS2.loc['Total Assets'].astype(float) 
    ER3 = BS3.loc["Total Stockholder Equity"].astype(float) / BS3.loc['Total Assets'].astype(float) 
    ER4 = BS4.loc["Total Stockholder Equity"].astype(float) / BS4.loc['Total Assets'].astype(float) 

    LTDR1 = BS1.loc['Long Term Debt'].astype(float) / BS1.loc['Total Assets'].astype(float) 
    LTDR2 = BS2.loc['Long Term Debt'].astype(float) / BS2.loc['Total Assets'].astype(float)
    LTDR3 = BS3.loc['Long Term Debt'].astype(float) / BS3.loc['Total Assets'].astype(float)
    LTDR4 = BS4.loc['Long Term Debt'].astype(float) / BS4.loc['Total Assets'].astype(float)

    GPM1 = IC1.loc['Gross Profit'].astype(float) / IC1.loc['Total Revenue'].astype(float) 
    GPM2 = IC2.loc['Gross Profit'].astype(float) / IC2.loc['Total Revenue'].astype(float) 
    GPM3 = IC3.loc['Gross Profit'].astype(float) / IC3.loc['Total Revenue'].astype(float) 
    GPM4 = IC4.loc['Gross Profit'].astype(float) / IC4.loc['Total Revenue'].astype(float) 

    NPM1 = IC1.loc['Net Income Applicable To Common Shares'].astype(float) / IC1.loc['Total Revenue'].astype(float)
    NPM2 = IC2.loc['Net Income Applicable To Common Shares'].astype(float) / IC2.loc['Total Revenue'].astype(float) 
    NPM3 = IC3.loc['Net Income Applicable To Common Shares'].astype(float) / IC3.loc['Total Revenue'].astype(float) 
    NPM4 = IC4.loc['Net Income Applicable To Common Shares'].astype(float) / IC4.loc['Total Revenue'].astype(float) 

    ROA1 = IC1.loc['Net Income Applicable To Common Shares'].astype(float) / BS1.loc['Total Assets'].astype(float)
    ROA2 = IC2.loc['Net Income Applicable To Common Shares'].astype(float) / BS2.loc['Total Assets'].astype(float)
    ROA3 = IC3.loc['Net Income Applicable To Common Shares'].astype(float) / BS3.loc['Total Assets'].astype(float)
    ROA4 = IC4.loc['Net Income Applicable To Common Shares'].astype(float) / BS4.loc['Total Assets'].astype(float)

    ROE1 = IC1.loc['Net Income Applicable To Common Shares'].astype(float) / BS1.loc['Total Stockholder Equity'].astype(float) 
    ROE2 = IC2.loc['Net Income Applicable To Common Shares'].astype(float) / BS2.loc['Total Stockholder Equity'].astype(float) 
    ROE3 = IC3.loc['Net Income Applicable To Common Shares'].astype(float) / BS3.loc['Total Stockholder Equity'].astype(float) 
    ROE4 = IC4.loc['Net Income Applicable To Common Shares'].astype(float) / BS4.loc['Total Stockholder Equity'].astype(float) 
    # print(BS1)
    EPS1 = IC1.loc['Net Income Applicable To Common Shares'].astype(float) / (BS1.loc['Common Stock'].astype(float) - BS1.loc['Gains Losses Not Affecting Retained Earnings'].astype(float)) 
    EPS2 = IC2.loc['Net Income Applicable To Common Shares'].astype(float) / (BS2.loc['Common Stock'].astype(float) - BS2.loc['Gains Losses Not Affecting Retained Earnings'].astype(float)) 
    EPS3 = IC3.loc['Net Income Applicable To Common Shares'].astype(float) / (BS3.loc['Common Stock'].astype(float) - BS3.loc['Gains Losses Not Affecting Retained Earnings'].astype(float)) 
    EPS4 = IC4.loc['Net Income Applicable To Common Shares'].astype(float) / (BS4.loc['Common Stock'].astype(float) - BS4.loc['Gains Losses Not Affecting Retained Earnings'].astype(float))

    def ratio(ratio_cat1,ratio_cat2,ratio_cat3,ratio_cat4):
        ratio_df = pd.DataFrame(columns = [options[0],options[1],options[2],options[3]])
        ratio_df[options[0]] = ratio_cat1.to_list()
        ratio_df[options[1]] = ratio_cat2.to_list()
        ratio_df[options[2]] = ratio_cat3.to_list()
        ratio_df[options[3]] = ratio_cat4.to_list()
        ratio_df.index = [str(i)[:4] for i in ratio_cat1.index] 
        fig = go.Figure(data=[
            go.Bar(name=str(ratio_df.index[0]), x=ratio_df.columns, y=ratio_df.iloc[0,:],marker_color='#5ab7ff',  marker_line=dict(width=1, color='#0078ff')),
            go.Bar(name=str(ratio_df.index[1]), x=ratio_df.columns, y=ratio_df.iloc[1,:],marker_color='#79da84',  marker_line=dict(width=1, color='#0078ff')),
            go.Bar(name=str(ratio_df.index[2]), x=ratio_df.columns, y=ratio_df.iloc[2,:],marker_color='#0078ff',  marker_line=dict(width=1, color='#0078ff')),
            go.Bar(name=str(ratio_df.index[3]), x=ratio_df.columns, y=ratio_df.iloc[3,:],marker_color='#e1efff',  marker_line=dict(width=1, color='#0078ff'))
        ])
        fig.update_layout(height=350, width=1000,barmode='group', margin=dict(l=0, r=0, t=0, b=0),paper_bgcolor="white",plot_bgcolor = '#f8fafd',legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1))
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#728391', gridcolor='white')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#728391', gridcolor='white')
        return fig

    main_df = pd.DataFrame(columns = ['Stocks Name','Dividend Yield', 'Short Ratio', 'Forward PE', 'Trailing PE','Previous Close','52 Week Change','52 Week High','52 Week Low'])
    main_df['Stocks Name'] = [options[0],options[1],options[2],options[3]]

    for index,category in enumerate(['dividendYield','shortRatio','forwardPE','trailingPE','previousClose','52WeekChange','fiftyTwoWeekHigh','fiftyTwoWeekLow']):
        main_df[main_df.columns[index+1]] = [stock1.info[category],stock2.info[category],stock3.info[category],stock4.info[category]]
    main_df.set_index('Stocks Name', inplace = True)
    main_df = main_df.transpose()



    st.markdown("""<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """, unsafe_allow_html=True)
    st.write('#### Ratio Comparison in last 4 years')
    col1, col2 = st.columns([1, 3])

    with col1:
        chart1 = st.selectbox(
            'Select Financial Ratio : ',
            ('Current Ratio', 'Total Asset Turnover', 'Total Debt Ratio','Debt/Equity','Equity Ratio','Long-term Debt Ratio'))
        
        chart2 = st.selectbox(
            'Profitability ratios : ',
            ('Net Profit Margin','Gross Profit Margin','Return on Assets (ROA)','Return on Equity (ROE)','Earning Per Share (EPS)')

        )
        
    
    with col2:
        if chart1 == 'Current Ratio':
            st.write('#### ',"Current Ratio")
            st.plotly_chart(ratio(CR1,CR2,CR3,CR4),use_container_width=True)

        if chart1 == 'Total Asset Turnover':
            st.write('#### ',"Total Asset Turnover")
            st.plotly_chart(ratio(TAT1,TAT2,TAT3,TAT4),use_container_width=True)

        if chart1 == 'Total Debt Ratio':
            st.write('#### ','Total Debt Ratio')
            st.plotly_chart(ratio(TDR1,TDR2,TDR3,TDR4),use_container_width=True)

        if chart1 == 'Debt/Equity':
            st.write('#### ','Debt/Equity')
            st.plotly_chart(ratio(DE1,DE2,DE3,DE4),use_container_width=True)
        if chart1 == 'Equity Ratio':
            st.write('#### ','Equity Ratio')
            st.plotly_chart(ratio(ER1,ER2,ER3,ER4),use_container_width=True)
        if chart1 == 'Long-term Debt Ratio':
            st.write('#### ','Long-term Debt Ratio')
            st.plotly_chart(ratio(LTDR1,LTDR2,LTDR3,LTDR4),use_container_width=True)

        if chart2 == 'Gross Profit Margin':
            st.write('#### ','Gross Profit Margin')
            st.plotly_chart(ratio(GPM1,GPM2,GPM3,GPM4),use_container_width=True)

        if chart2 == 'Net Profit Margin':
            st.write('#### ','Net Profit Margin')
            st.plotly_chart(ratio(NPM1,NPM2,NPM3,NPM4),use_container_width=True)
        if chart2 == 'Return on Assets (ROA)':
            st.write('#### ','Return on Assets (ROA)')
            st.plotly_chart(ratio(ROA1,ROA2,ROA3,ROA4),use_container_width=True)
        if chart2 == 'Return on Equity (ROE)':
            st.write('#### ','Return on Equity (ROE)')
            st.plotly_chart(ratio(ROE1,ROE2,ROE3,ROE4),use_container_width=True)
        if chart2 == 'Earning Per Share (EPS)':
            st.write('#### ','Earning Per Share (EPS)')
            st.plotly_chart(ratio(EPS1,EPS2,EPS3,EPS4),use_container_width=True)

        
    font_css = """
        <style>
        button[data-baseweb="tab"] {
        font-size: 16px;
        }
        </style>
        """

    st.write(font_css, unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Balance Sheet", "CashFlow Statement", "Financials","Earnings"])
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
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #79da84;
            color:black;
        }
        div.stButton > button:hover {
            background-color: #0078ff;
            color:white;
            }
        </style>""", unsafe_allow_html=True)
    with tab1:
        col1, col2 = st.columns([1, 4])

        table = ''
        with col1:
            
            if st.button(options[0]):
                table = options[0]
            if st.button(options[1]):
                table = options[1]
            if st.button(options[2]):
                table = options[2]
            if st.button(options[3]):
                table = options[3]
        with col2:
            
            if table == options[0]:
                st.write('#### ',options[0])
                st.write(plotly_table(stock1.balancesheet),use_container_width=True)
            elif table == options[1]:
                st.write('#### ',options[1])
                st.write(plotly_table(stock2.balancesheet),use_container_width=True)
            elif table == options[2]:
                st.write('#### ',options[2])
                st.write(plotly_table(stock3.balancesheet),use_container_width=True)
            elif table == options[3]:
                st.write('#### ', options[3])
                st.write(plotly_table(stock4.balancesheet),use_container_width=True)
            else:
                st.write('#### ',options[0])
                st.plotly_chart(plotly_table(stock1.balancesheet), use_container_width=True)
    with tab2:
        col1, col2 = st.columns([1, 3])

        table = ''
        with col1:
            if st.button(options[0],key="1"):
                table = options[0]
            if st.button(options[1],key="2"):
                table = options[1]
            if st.button(options[2],key="3"):
                table = options[2]
            if st.button(options[3],key="4"):
                table = options[3]
        with col2:
            if table == options[0]:
                st.write('#### ',options[0])
                st.write(plotly_table(stock1.cashflow),use_container_width=True)
            elif table == options[1]:
                st.write('#### ',options[1])
                st.write(plotly_table(stock2.cashflow),use_container_width=True)
            elif table == options[2]:
                st.write('#### ',options[2])
                st.write(plotly_table(stock3.cashflow),use_container_width=True)
            elif table == options[3]:
                st.write('#### ',options[3])
                st.write(plotly_table(stock4.cashflow),use_container_width=True)
            else:
                st.write('#### ',options[0])
                st.plotly_chart(plotly_table(stock1.cashflow), use_container_width=True)
    with tab3:
        col1, col2 = st.columns([1, 3])

        table = ''
        with col1:
            if st.button(options[0],key="11"):
                table = options[0]
            if st.button(options[1],key="21"):
                table = options[1]
            if st.button(options[2],key="31"):
                table = options[2]
            if st.button(options[3],key="41"):
                table = options[3]
        with col2:
            if table == options[0]:
                st.write('#### ',options[0])
                st.write(plotly_table(stock1.financials),use_container_width=True)
            elif table == options[1]:
                st.write('#### ',options[1])
                st.write(plotly_table(stock2.financials),use_container_width=True)
            elif table == options[2]:
                st.write('#### ',options[2])
                st.write(plotly_table(stock3.financials),use_container_width=True)
            elif table == options[3]:
                st.write('#### ',options[3])
                st.write(plotly_table(stock4.financials),use_container_width=True)
            else:
                st.write('#### ',options[0])
                st.plotly_chart(plotly_table(stock1.financials), use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns([1, 3])

        table = ''
        with col1:
            if st.button(options[0],key="14"):
                table = options[0]
            if st.button(options[1],key="24"):
                table = options[1]
            if st.button(options[2],key="34"):
                table = options[2]
            if st.button(options[3],key="44"):
                table = options[3]
        with col2:
            if table == options[0]:
                st.write('#### ',options[0])
                st.write(plotly_table(stock1.earnings),use_container_width=True)
            elif table == options[1]:
                st.write('#### ',options[1])
                st.write(plotly_table(stock2.earnings),use_container_width=True)
            elif table == options[2]:
                st.write('#### ',options[2])
                st.write(plotly_table(stock3.earnings),use_container_width=True)
            elif table == options[3]:
                st.write('#### ',options[3])
                st.write(plotly_table(stock4.earnings),use_container_width=True)
            else:
                st.write('#### ',options[0])
                st.plotly_chart(plotly_table(stock1.earnings), use_container_width=True)
    
        
    st.write('#### Close Price')
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
    new_df1 = stock1.history(period = num_period)
    new_df2 = stock2.history(period = num_period)
    new_df3 = stock3.history(period = num_period)
    new_df4 = stock4.history(period = num_period)
    def figure_close(data1, data2, data3, data4):
        fig_close = make_subplots(rows=1, cols=4,subplot_titles=(options[0],options[1],options[2],options[3]))

        fig_close.append_trace(go.Scatter(
            x=df1.index,
            y=df1.Close, name = options[0],line = dict( width=4,color ='#5ab7ff'),
        ), row=1, col=1)

        fig_close.append_trace(go.Scatter(
            x=df2.index,
            y=df2.Close, name = options[1],line = dict( width=4,color = '#79da84'),
        ), row=1, col=2)


        fig_close.append_trace(go.Scatter(
            x=df3.index,
            y=df3.Close, name = options[2],line = dict( width=4,color = '#0078ff'),
        ), row=1, col=3)

        fig_close.append_trace(go.Scatter(
            x=df4.index,
            y=df4.Close, name = options[3],line = dict( width=4,color = 'black'),
        ), row=1, col=4)
        
        
        fig_close.update_layout(height=250, width=1600, showlegend = False,paper_bgcolor="white",plot_bgcolor = '#f8fafd',margin=dict(l=0, r=0, t=0, b=0))
        fig_close.update_xaxes(showline=True, linewidth=2, linecolor='#0078ff', gridcolor='white')
        fig_close.update_yaxes(showline=True, linewidth=2, linecolor='#0078ff', gridcolor='white')
        return fig_close
    

    if num_period == '':
       
        st.plotly_chart(figure_close(new_df1,new_df2,new_df3,new_df4), use_container_width=True)
    else:
        st.plotly_chart(figure_close(df1,df2,df3,df4), use_container_width=True)
    st.markdown("""<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """, unsafe_allow_html=True)
    
 
    fig_table = plotly_table(main_df)
    fig_table.update_layout(height = 350)
    st.plotly_chart(fig_table,use_container_width=True)

    
    open_stock = pd.concat([df1['Open'],df2['Open'],df3['Open'],df4['Open']], axis = 1)
    open_stock.columns = [options[0],options[1],options[2],options[3]]
    open_stock.dropna(inplace = True)
    st.markdown("""<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """, unsafe_allow_html=True)
    st.write('#### Correlation Between Stocks')
    col1, col2 = st.columns([2,3])
    with col1:
        fig = go.Figure(data=go.Splom(
                    dimensions=[dict(label=options[0],
                                    values=df1['Open']),
                                dict(label=options[1],
                                    values=df2['Open']),
                                dict(label=options[2],
                                    values=df3['Open']),
                                dict(label=options[3],
                                    values=df4['Open'])],
                    showupperhalf=False,diagonal_visible=False,
                    marker=dict(color='#0078ff',
                                showscale=False, # colors encode categorical variables
                                line_color='white', line_width=0.6)
                    ))


        fig.update_layout(
            dragmode='select',
            width=700,
            height=600,
            hovermode='closest',
        )

        st.plotly_chart(fig)
    with col2:
        fig = plotly_table(open_stock.corr().round(3))
        fig.update_layout( height= 200, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    st.write('Select 4 stocks')
    print(e)


