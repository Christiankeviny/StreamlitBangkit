import streamlit as st
import pandas as pd
import matplotlib as plt
import os

filepath1= os.path.join(os.path.dirname(__file__), 'dl_monthly_aqi.csv')
df1= pd.read_csv(filepath1)
filepath2= os.path.join(os.path.dirname(__file__), 'dl_yearly_aqi.csv')
df2= pd.read_csv(filepath2)
filepath3= os.path.join(os.path.dirname(__file__), 'gy_monthly_aqi.csv')
df3= pd.read_csv(filepath3)
filepath4= os.path.join(os.path.dirname(__file__), 'gy_yearly_aqi.csv')
df4= pd.read_csv(filepath4)

st.title('Tugas Streamlit Cloud and lokal')
tab1, tab2, tab3 = st.tabs(["Dingling", "Guanyuan", "Compare Graph"])
 
with tab1:
    st.header("Dingling City")

    with st.container():
        
        pilihan = st.selectbox("Select View", ["Monthly", "Yearly"],key="select_view_1")   
        if pilihan == "Monthly":
            st.subheader("Monthly Data")
            st.caption  ('Table 1. tabel bulanan ')
            st.dataframe(data=df1, width=500, height=450)

        elif pilihan == "Yearly":
            st.subheader("Yearly Data")
            st.caption  ('Table 2. Kota Dingling tahunan ')
            st.dataframe(data=df2.style.format({"year": "{:d}"}),width=500, height=210 )
    st.write("terlihat pada table 1, dan table 2, data Dingling mengalami peningkatan kualitas udara dari tahun 2013 ke 2017 ")

with tab2:
    st.header("Guanyuan")
    pilihan = st.selectbox("Select View", ["Monthly", "Yearly"],key="select_view_2")   
    if pilihan == "Monthly":
        st.subheader("Monthly Data")
        st.caption  ('Table 3. Kota Guanyuan bulanan ')
        st.dataframe(data=df3, width=500, height=450)

    elif pilihan == "Yearly":
        st.subheader("Yearly Data")
        st.caption  ('Table 4. Kota Guanyuan tahunan ')
        st.dataframe(data=df4.style.format({"year": "{:d}"}), width=500, height=210)
    st.write("terlihat pada table 3, dan table 4, Guanyuan berada di kategori light polluted lalu meningkat kualitas udaranya dari tahun 2013 ke 2016 setelah itu memburuk kembali pada tahun 2017")

with tab3:
    st.header("Comparing Graph")

    with st.container():
        
        pilihan3 = st.selectbox(label="select your timeframe",options=("Monthly", "Yearly"),key="select_view_3")
        if pilihan3 == "Monthly":
            st.subheader("Monthly Data")
            plt.figure(figsize=(10, 6))
            plt.plot(df1['month'], df1['AQI'], marker='o', linestyle='-', color='b', label='Dingling AQI')
            plt.plot(df3['month'], df3['AQI'], marker='o', linestyle='-', color='c', label='Guanyuan AQI')

            # label and judul
            plt.xlabel('Month')
            plt.ylabel('AQI')
            plt.title('Mean AQI by Month')
            plt.grid(True)

            # legend
            plt.legend()

            # plotting
            st.pyplot(plt)
            st.caption('Figure 1. Grafik perbandingan terhadap monthly ')

        elif pilihan3 == "Yearly":
            st.subheader("Yearly Data")
            plt.figure(figsize=(10, 6))
            plt.plot(df2['year'], df2['AQI'], marker='o', linestyle='-', color='b', label='Dingling AQI')
            plt.plot(df4['year'], df4['AQI'], marker='o', linestyle='-', color='c', label='Guanyuan AQI')

            # label and judul
            plt.xlabel('Year')
            plt.ylabel(' AQI')
            plt.title('Mean AQI by Year')
            plt.grid(True)

            # legend
            plt.legend()

            # plotting
            st.pyplot(plt)
            st.caption('Figure 2. Grafik perbandingan terhadap yearly ')
    st.write("terlihat bahwa kesimpulan yang sebelumnya sangat sesuai dengan grafik garis pada figure 1, dan figure 2, dimana semakin besar nilainya, maka semakin berpolusi tempat tersebut")    