import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Kuesioner", layout="wide")

# ==============================
# STYLE GLOBAL
# ==============================
PRIMARY = "#2563eb"
SUCCESS = "#16a34a"
WARNING = "#f59e0b"
DANGER = "#dc2626"

px.defaults.template = "plotly_white"

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx", engine="openpyxl")

df = load_data()
df_numeric = df.select_dtypes(include="number")

st.title("📊 Dashboard Analisis Kuesioner")
st.markdown("Visualisasi Profesional & Modern")

# ==============================
# KPI SECTION
# ==============================
total_responden = len(df)
mean_total = df_numeric.mean().mean()

col1, col2 = st.columns(2)
col1.metric("Total Responden", total_responden)
col2.metric("Indeks Kepuasan", f"{mean_total:.2f} / 5")

st.divider()

# =====================================================
# 1️⃣ DISTRIBUSI KESELURUHAN
# =====================================================
st.subheader("Distribusi Jawaban Keseluruhan")

all_values = df_numeric.values.flatten()
all_series = pd.Series(all_values)

dist = all_series.value_counts().sort_index().reset_index()
dist.columns = ["Skor", "Jumlah"]

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=dist["Skor"],
    y=dist["Jumlah"],
    marker_color=PRIMARY,
    text=dist["Jumlah"],
    textposition="outside"
))

fig1.update_layout(
    height=400,
    xaxis_title="Skor",
    yaxis_title="Jumlah Respon",
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 2️⃣ PIE DONUT MODERN
# =====================================================
st.subheader("Proporsi Jawaban")

fig2 = go.Figure(go.Pie(
    labels=dist["Skor"],
    values=dist["Jumlah"],
    hole=0.6,
    marker_colors=["#1d4ed8", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"]
))

fig2.update_layout(height=400)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3️⃣ STACKED BAR ELEGAN
# =====================================================
st.subheader("Distribusi per Pertanyaan")

df_melt = df_numeric.melt(var_name="Pertanyaan", value_name="Skor")
stacked = df_melt.groupby(["Pertanyaan", "Skor"]).size().reset_index(name="Jumlah")

fig3 = px.bar(
    stacked,
    x="Pertanyaan",
    y="Jumlah",
    color="Skor",
    barmode="stack",
    color_continuous_scale="Blues"
)

fig3.update_layout(height=500)
st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# 4️⃣ RATA-RATA PER PERTANYAAN (CLEAN STYLE)
# =====================================================
st.subheader("Rata-rata Skor per Pertanyaan")

mean_scores = df_numeric.mean().reset_index()
mean_scores.columns = ["Pertanyaan", "Rata-rata"]

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=mean_scores["Pertanyaan"],
    y=mean_scores["Rata-rata"],
    marker_color=PRIMARY,
    text=mean_scores["Rata-rata"].round(2),
    textposition="outside"
))

fig4.update_layout(
    yaxis=dict(range=[0,5]),
    height=450,
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# 5️⃣ POSITIF NETRAL NEGATIF (WARNA PSIKOLOGIS)
# =====================================================
st.subheader("Distribusi Sentimen Jawaban")

def kategori(x):
    if x >= 4:
        return "Positif"
    elif x == 3:
        return "Netral"
    else:
        return "Negatif"

kategori_series = all_series.apply(kategori)
kategori_count = kategori_series.value_counts().reset_index()
kategori_count.columns = ["Kategori", "Jumlah"]

color_map = {
    "Positif": SUCCESS,
    "Netral": WARNING,
    "Negatif": DANGER
}

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    x=kategori_count["Kategori"],
    y=kategori_count["Jumlah"],
    marker_color=[color_map[k] for k in kategori_count["Kategori"]],
    text=kategori_count["Jumlah"],
    textposition="outside"
))

fig5.update_layout(height=400, showlegend=False)

st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# 6️⃣ GAUGE PREMIUM
# =====================================================
st.subheader("Indeks Kepuasan")

fig6 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=mean_total,
    number={'suffix': " / 5"},
    gauge={
        'axis': {'range': [1,5]},
        'bar': {'color': PRIMARY},
        'steps': [
            {'range': [1,2], 'color': "#fee2e2"},
            {'range': [2,3], 'color': "#fef3c7"},
            {'range': [3,4], 'color': "#dbeafe"},
            {'range': [4,5], 'color': "#dcfce7"},
        ]
    }
))

fig6.update_layout(height=350)
st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# 7️⃣ HEATMAP MODERN
# =====================================================
st.subheader("Korelasi Antar Pertanyaan")

corr = df_numeric.corr()

fig7 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues"
)

fig7.update_layout(height=500)
st.plotly_chart(fig7, use_container_width=True)
