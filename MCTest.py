import datetime
import streamlit as st
import pandas as pd
st.title('Market Cap Rank Positioning Changes')
st.subheader('Note this is only a prototype. Data from coincodex.com')
st.write('Only the 1st of each month is available right now. The table is interactive and can be sorted by difference. ')
st.write('0 is no change, Positive number = Increase in rank, Negative number = Decrease in rank')
d1= st.date_input("First Date", value=None,min_value=datetime.datetime(2013, 5, 1), max_value=datetime.datetime.now())
st.write("First Date is:", d1)
d2 = st.date_input("Second Date", value=None,min_value=datetime.datetime(2013, 5, 1), max_value=datetime.datetime.now())
st.write("Second Date is:", d2)
if d1==None:
    st.write('First Date not selected yet')
if d2==None:
    st.write('Second Date not selected yet')
if d1!=None and d2!=None:
    try:
        s3_1='s3://crypto-month-data/'+str(d1)+'.parquet'
        s3_2='s3://crypto-month-data/'+str(d2)+'.parquet'
        df1=pd.read_parquet(s3_1)
        df2=pd.read_parquet(s3_2)
        df3=pd.merge(df1, df2, on='symbol')
        df3["Difference"]=(df3['Rank_y'])-(df3['Rank_x'])
        df3=df3.drop(['display_symbol_x','aliases_x','shortname_x','last_price_usd_x','volume_24_usd_x','market_cap_usd_x','Rank_y','display_symbol_y'], axis=1)
        df3=df3.drop(['name_y','aliases_y','shortname_y','last_price_usd_y','volume_24_usd_y','market_cap_usd_y'], axis=1)
        st.dataframe(df3,hide_index=True)
    except FileNotFoundError or OSError::
        st.header(' Error. Reminder only the first of each month can be selected. Please select a different date.')
