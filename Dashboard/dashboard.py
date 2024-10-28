# code end to end ngubah all_data_chinadf.csv yg udah bersih jd bagian kotanya sampe nampilin di streamlit lokal dan cloud (online), komparasi grafik
# dan kesimpulan dari hasil data dan komparasi grafik

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

filepath5= os.path.join(os.path.dirname(__file__), 'all_data_chinadf.csv')
df= pd.read_csv(filepath5)

#Bikin range values untuk SUBINDEX AQI china dari paling baik ke paling buruk
pollutant_breakpoints = {
    'PM2.5': [(0, 35), (35, 75), (75, 115), (115, 150), (150, 250), (250, 350), (350, 500)],
    'PM10': [(0, 50), (50, 150), (150, 250), (250, 350), (350, 420), (420, 500), (500, 600)],
    'SO2': [(0, 50), (50, 150), (150, 475), (475, 800), (800, 1600), (1600, 2100), (2100, 2620)],
    'NO2': [(0, 40), (40, 80), (80, 180), (180, 280), (280, 565), (565, 750), (750, 940)],
    'CO': [(0, 2), (2, 4), (4, 14), (14, 24), (24, 36), (36, 48), (48, 60)],
    'O3': [(0, 100), (100, 160), (160, 215), (215, 265), (265, 800)]
}

#Bikin range values untuk INDEX AQI China dari paling baik ke paling buruk
aqi_breakpoints = [(0, 50), (51, 100), (101, 150), (151, 200), (201, 300), (301, 400), (401, 500)]

# Bikin function penentu kategori berdasarkan range
def classify_aqi_category(aqi):
    if aqi <= 50:
        return 'Excellent'
    elif 51 <= aqi <= 100:
        return 'Good'
    elif 101 <= aqi <= 150:
        return 'Lightly Polluted'
    elif 151 <= aqi <= 200:
        return 'Moderately Polluted'
    elif 201 <= aqi <= 300:
        return 'Heavily Polluted'
    elif 301 <= aqi <= 400:
        return 'Severely Polluted'
    elif 401 <= aqi <= 500:
        return 'Extremely Polluted'
    else:
        return 'Invalid AQI'

# Bikin function untuk rumus AQI
def calculate_subindex(concentration, breakpoints):
    for i, (c_low, c_high) in enumerate(breakpoints):
        if c_low <= concentration <= c_high:
            aqi_low, aqi_high = aqi_breakpoints[i]
            return aqi_low + (aqi_high - aqi_low) * (concentration - c_low) / (c_high - c_low)
    return None

# Bikin variable untuk function berdasarkan rownya trus return nilai max sub-index sebagai nilai AQI
def calculate_aqi_for_row(row):
    pollutant_concentrations = {
        'PM2.5': row['PM2.5'],
        'PM10': row['PM10'],
        'SO2': row['SO2'],
        'NO2': row['NO2'],
        'CO': row['CO'],
        'O3': row['O3']
    }

    sub_indexes = {}
    for pollutant, concentration in pollutant_concentrations.items():
        if pollutant in pollutant_breakpoints and pd.notnull(concentration):
            subindex = calculate_subindex(concentration, pollutant_breakpoints[pollutant])
            if subindex is not None:
                sub_indexes[pollutant] = subindex

    if sub_indexes:
        return max(sub_indexes.values())
    return None

def calculate_aqi_by_station(df):
    # Bikin Split data berdasarkan station/kota
    Dingling_df = df[df['station'] == 'Dingling'].copy()
    Guanyuan_df = df[df['station'] == 'Guanyuan'].copy()
    return Dingling_df, Guanyuan_df

def create_dingling_yearly_and_monthly_df(Dingling_df):
    # Gabungin tahun, bulan, hari, jam menjadi satu array variable datetime
    Dingling_df['datetime'] = pd.to_datetime(Dingling_df[['year', 'month', 'day', 'hour']])

    # Apply perhitungan AQI untuk setiap row di DataFrame (Dingling_df)
    Dingling_df['AQI'] = Dingling_df.apply(calculate_aqi_for_row, axis=1)

    # Extract tahun dan bulan dari datetime
    Dingling_df['year'] = Dingling_df['datetime'].dt.year
    Dingling_df['month'] = Dingling_df['datetime'].dt.month

    # Menghitung rata-rata AQI tiap tahun
    Dingling_yearly_aqi = Dingling_df.groupby('year')['AQI'].mean().reset_index()
    Dingling_yearly_aqi['AQI'] = Dingling_yearly_aqi['AQI'].round(0).astype(int) # Membulatkan dan mengubah float menjadi integer
    Dingling_yearly_aqi['AQI_Category'] = Dingling_yearly_aqi['AQI'].apply(classify_aqi_category) # Apply kategori AQI ke rata-rata AQI tahunan
    df2= Dingling_yearly_aqi

    # Menghitung rata-rata AQI tiap bulan
    Dingling_monthly_aqi = Dingling_df.groupby('month')['AQI'].mean().reset_index() # Membulatkan dan mengubah float menjadi integer
    Dingling_monthly_aqi['AQI'] = Dingling_monthly_aqi['AQI'].round(0).astype(int) # Apply kategori AQI ke rata-rata AQI bulanan
    Dingling_monthly_aqi['AQI_Category'] = Dingling_monthly_aqi['AQI'].apply(classify_aqi_category)
    df1=Dingling_monthly_aqi
    # Mengeluarkan pivot tabel rata-rata AQI dan kategori AQI pertahun dan perbulan
    return df2, df1

def create_guanyuan_yearly_and_monthly_df(Guanyuan_df):
    # Gabungin tahun, bulan, hari, jam menjadi satu array variable datetime
    Guanyuan_df['datetime'] = pd.to_datetime(Guanyuan_df[['year', 'month', 'day', 'hour']])

    # Apply perhitungan AQI untuk setiap row di DataFrame (Guanyuan_df)
    Guanyuan_df['AQI'] = Guanyuan_df.apply(calculate_aqi_for_row, axis=1)

    # Extract tahun dan bulan dari datetime
    Guanyuan_df['year'] = Guanyuan_df['datetime'].dt.year
    Guanyuan_df['month'] = Guanyuan_df['datetime'].dt.month

    # Menghitung rata-rata AQI tiap tahun
    Guanyuan_yearly_aqi = Guanyuan_df.groupby('year')['AQI'].mean().reset_index()
    Guanyuan_yearly_aqi['AQI'] = Guanyuan_yearly_aqi['AQI'].round(0).astype(int) # Membulatkan dan mengubah float menjadi integer
    Guanyuan_yearly_aqi['AQI_Category'] = Guanyuan_yearly_aqi['AQI'].apply(classify_aqi_category) # Apply kategori AQI ke rata-rata AQI tahunan
    df4 = Guanyuan_yearly_aqi

    # Menghitung rata-rata AQI tiap bulan
    Guanyuan_monthly_aqi = Guanyuan_df.groupby('month')['AQI'].mean().reset_index() # Membulatkan dan mengubah float menjadi integer
    Guanyuan_monthly_aqi['AQI'] = Guanyuan_monthly_aqi['AQI'].round(0).astype(int) # Apply kategori AQI ke rata-rata AQI bulanan
    Guanyuan_monthly_aqi['AQI_Category'] = Guanyuan_monthly_aqi['AQI'].apply(classify_aqi_category)
    df3 = Guanyuan_monthly_aqi
    # Mengeluarkan pivot tabel rata-rata AQI dan kategori AQI pertahun dan perbulan
    return df3, df4

# call back Dingling_df dan Guanyuan_df  
Dingling_df, Guanyuan_df = calculate_aqi_by_station(df)

# call back dataframe tahunan and bulanan untuk setiap station/city
df2, df1 = create_dingling_yearly_and_monthly_df(Dingling_df)
df3, df4 = create_guanyuan_yearly_and_monthly_df(Guanyuan_df)

# kode buat streamlit nampilin dataframe, komparasi grafik dan kesimpulan secara lokal pake streamlit run dashboard.py di terminal
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
    st.write("Nilai tertinggi dan terendah pada kota Dingling ada pada bulan Maret di angka 130 dan bulan Agustus pada angka 84, pada kota Guanyuan nilai tertinggi ada pada bulan December di angka 153 dan nilai terendah di bulan Agustus di angka 101")
    st.write("Alasan mengapa pada agustus sebenarnya bisa di explore lagi dengan mengamati rata-rata nilai curah hujan tiap bulannya dari tahun ke tahun")