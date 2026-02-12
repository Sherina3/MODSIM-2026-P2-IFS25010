import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Kuesioner", layout="wide")

st.title("📊 Dashboard Visualisasi Data Kuesioner")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_excel("data_kuesioner.xlsx", engine="openpyxl")
    return df

df = load_data()

st.subheader("Preview Data")
st.dataframe(df)

# Pastikan hanya kolom numerik yang dianalisis
df_numeric = df.select_dtypes(include="number")

# ===============================
# 1️⃣ BAR CHART DISTRIBUSI KESELURUHAN
# ===============================
st.header("1. Distribusi Jawaban Keseluruhan")

all_values = df_numeric.values.flatten()
all_series = pd.Series(all_values)

distribusi = all_series.value_counts().sort_index().reset_index()
distribusi.columns = ["Skor", "Jumlah"]

fig1 = px.bar(distribusi, x="Skor", y="Jumlah",
              title="Distribusi Jawaban Keseluruhan",
              text="Jumlah")

st.plotly_chart(fig1, use_container_width=True)

# ===============================
# 2️⃣ PIE CHART PROPORSI
# ===============================
st.header("2. Proporsi Jawaban Keseluruhan")

fig2 = px.pie(distribusi, names="Skor", values="Jumlah",
              title="Proporsi Jawaban Keseluruhan")

st.plotly_chart(fig2, use_container_width=True)

# ===============================
# 3️⃣ STACKED BAR PER PERTANYAAN
# ===============================
st.header("3. Distribusi Jawaban per Pertanyaan")

df_melt = df_numeric.melt(var_name="Pertanyaan", value_name="Skor")

stacked = df_melt.groupby(["Pertanyaan", "Skor"]).size().reset_index(name="Jumlah")

fig3 = px.bar(stacked,
              x="Pertanyaan",
              y="Jumlah",
              color="Skor",
              title="Distribusi Jawaban per Pertanyaan",
              barmode="stack")

st.plotly_chart(fig3, use_container_width=True)

# ===============================
# 4️⃣ RATA-RATA SKOR PER PERTANYAAN
# ===============================
st.header("4. Rata-rata Skor per Pertanyaan")

mean_scores = df_numeric.mean().reset_index()
mean_scores.columns = ["Pertanyaan", "Rata-rata"]

fig4 = px.bar(mean_scores,
              x="Pertanyaan",
              y="Rata-rata",
              title="Rata-rata Skor per Pertanyaan",
              text="Rata-rata")

st.plotly_chart(fig4, use_container_width=True)

# ===============================
# 5️⃣ DISTRIBUSI POSITIF, NETRAL, NEGATIF
# ===============================
st.header("5. Distribusi Kategori Jawaban")

def kategori(skor):
    if skor >= 4:
        return "Positif"
    elif skor == 3:
        return "Netral"
    else:
        return "Negatif"

kategori_series = all_series.apply(kategori)
kategori_count = kategori_series.value_counts().reset_index()
kategori_count.columns = ["Kategori", "Jumlah"]

fig5 = px.bar(kategori_count,
              x="Kategori",
              y="Jumlah",
              title="Distribusi Positif, Netral, Negatif",
              text="Jumlah")

st.plotly_chart(fig5, use_container_width=True)

# ===============================
# 🎁 BONUS 1: HEATMAP KORELASI
# ===============================
st.header("Bonus: Heatmap Korelasi Antar Pertanyaan")

corr = df_numeric.corr()

fig6 = px.imshow(corr,
                 text_auto=True,
                 aspect="auto",
                 title="Heatmap Korelasi")

st.plotly_chart(fig6, use_container_width=True)

# ===============================
# 🎁 BONUS 2: BOX PLOT
# ===============================
st.header("Bonus: Boxplot Distribusi Skor")

fig7 = px.box(df_melt,
              x="Pertanyaan",
              y="Skor",
              title="Boxplot Distribusi Skor per Pertanyaan")

st.plotly_chart(fig7, use_container_width=True)
