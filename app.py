import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Kuesioner", layout="wide")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx", engine="openpyxl")

df = load_data()
df_numeric = df.select_dtypes(include="number")

# ===============================
# SIDEBAR FILTER
# ===============================
st.sidebar.header("⚙️ Filter Data")

selected_questions = st.sidebar.multiselect(
    "Pilih Pertanyaan",
    df_numeric.columns,
    default=df_numeric.columns
)

df_filtered = df_numeric[selected_questions]

# ===============================
# HEADER
# ===============================
st.title("📊 Dashboard Analisis Kuesioner")
st.markdown("Visualisasi interaktif untuk analisis data survei")

# ===============================
# KPI CARDS
# ===============================
total_responden = len(df)
rata_total = df_filtered.mean().mean()
skor_tertinggi = df_filtered.max().max()
skor_terendah = df_filtered.min().min()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Responden", total_responden)
col2.metric("Rata-rata Skor", f"{rata_total:.2f}")
col3.metric("Skor Tertinggi", skor_tertinggi)
col4.metric("Skor Terendah", skor_terendah)

st.divider()

# ===============================
# TABS
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribusi",
    "📈 Analisis Pertanyaan",
    "😊 Kategori Jawaban",
    "🎁 Insight Tambahan"
])

# ==================================================
# TAB 1 — DISTRIBUSI
# ==================================================
with tab1:

    all_values = df_filtered.values.flatten()
    all_series = pd.Series(all_values)

    distribusi = all_series.value_counts().sort_index().reset_index()
    distribusi.columns = ["Skor", "Jumlah"]

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            distribusi,
            x="Skor",
            y="Jumlah",
            text="Jumlah",
            color="Skor",
            color_continuous_scale="Blues",
            title="Distribusi Jawaban Keseluruhan"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            distribusi,
            names="Skor",
            values="Jumlah",
            hole=0.4,
            title="Proporsi Jawaban"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==================================================
# TAB 2 — ANALISIS PER PERTANYAAN
# ==================================================
with tab2:

    df_melt = df_filtered.melt(var_name="Pertanyaan", value_name="Skor")
    stacked = df_melt.groupby(["Pertanyaan", "Skor"]).size().reset_index(name="Jumlah")

    fig_stack = px.bar(
        stacked,
        x="Pertanyaan",
        y="Jumlah",
        color="Skor",
        barmode="stack",
        title="Distribusi Jawaban per Pertanyaan"
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    # Rata-rata
    mean_scores = df_filtered.mean().reset_index()
    mean_scores.columns = ["Pertanyaan", "Rata-rata"]

    fig_mean = px.bar(
        mean_scores,
        x="Pertanyaan",
        y="Rata-rata",
        text="Rata-rata",
        color="Rata-rata",
        color_continuous_scale="Viridis",
        title="Rata-rata Skor per Pertanyaan"
    )
    st.plotly_chart(fig_mean, use_container_width=True)

# ==================================================
# TAB 3 — KATEGORI
# ==================================================
with tab3:

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

    fig_kategori = px.bar(
        kategori_count,
        x="Kategori",
        y="Jumlah",
        text="Jumlah",
        color="Kategori",
        title="Distribusi Positif, Netral, Negatif"
    )

    st.plotly_chart(fig_kategori, use_container_width=True)

    # Gauge Chart Kepuasan
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rata_total,
        title={'text': "Indeks Kepuasan (Rata-rata Skor)"},
        gauge={
            'axis': {'range': [1, 5]},
            'bar': {'color': "darkblue"},
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

# ==================================================
# TAB 4 — BONUS INSIGHT
# ==================================================
with tab4:

    # Heatmap Korelasi
    corr = df_filtered.corr()

    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Heatmap Korelasi Antar Pertanyaan"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Radar Chart
    radar = df_filtered.mean()

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=radar.values,
        theta=radar.index,
        fill='toself'
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        title="Radar Chart Rata-rata Skor"
    )

    st.plotly_chart(fig_radar, use_container_width=True)

# ===============================
# DOWNLOAD DATA
# ===============================
st.sidebar.download_button(
    label="📥 Download Data (CSV)",
    data=df.to_csv(index=False),
    file_name="data_kuesioner.csv",
    mime="text/csv"
)
