import streamlit as st
import pandas as pd

# Judul aplikasi
st.title("Dashboard Data Kuesioner")

# Membaca file Excel
@st.cache_data
def load_data():
    data = pd.read_excel("data_kuesioner.xlsx")
    return data

df = load_data()

# Menampilkan data
st.subheader("Data Kuesioner")
st.dataframe(df)

# Informasi dasar
st.subheader("Informasi Dataset")
st.write("Jumlah Baris:", df.shape[0])
st.write("Jumlah Kolom:", df.shape[1])

# Statistik deskriptif (jika ada data numerik)
st.subheader("Statistik Deskriptif")
st.write(df.describe())

# Pilih kolom untuk dianalisis
st.subheader("Visualisasi Data")
kolom = st.selectbox("Pilih kolom:", df.columns)

if df[kolom].dtype == "object":
    # Jika kolom kategori
    st.bar_chart(df[kolom].value_counts())
else:
    # Jika kolom numerik
    st.line_chart(df[kolom])
