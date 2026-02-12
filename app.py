import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Executive Survey Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# COLOR SYSTEM (SOFT MODERN)
# =============================
COLORS = {
    "primary": "#1f2937",
    "accent": "#2563eb",
    "positive": "#22c55e",
    "neutral": "#f59e0b",
    "negative": "#ef4444",
    "background": "#f9fafb"
}

px.defaults.template = "plotly_white"

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx", engine="openpyxl")

df = load_data()
df_num = df.select_dtypes(include="number")

# =============================
# HEADER
# =============================
st.markdown("## 📊 Executive Survey Analytics")
st.caption("Clean • Professional • Insight Driven")

# =============================
# KPI SECTION
# =============================
mean_total = df_num.mean().mean()
total_responden = len(df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Responden", total_responden)
col2.metric("Rata-rata Skor", f"{mean_total:.2f} / 5")
col3.metric(
    "Kategori Kepuasan",
    "Tinggi" if mean_total >= 4 else "Sedang" if mean_total >= 3 else "Rendah"
)

st.divider()

# =========================================================
# 1️⃣ DISTRIBUSI KESELURUHAN (ELEGANT BAR)
# =========================================================
all_values = df_num.values.flatten()
series = pd.Series(all_values)

dist = series.value_counts().sort_index()

fig1 = go.Figure()

fig1.add_bar(
    x=dist.index,
    y=dist.values,
    marker_color=COLORS["accent"],
    text=dist.values,
    textposition="outside",
    marker_line_width=0
)

fig1.update_layout(
    title="Distribusi Jawaban Keseluruhan",
    height=420,
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 2️⃣ DONUT MODERN MINIMAL
# =========================================================
fig2 = go.Figure(go.Pie(
    labels=dist.index,
    values=dist.values,
    hole=0.65,
    textinfo="percent+label",
    marker=dict(
        colors=["#1d4ed8","#3b82f6","#60a5fa","#93c5fd","#bfdbfe"]
    )
))

fig2.update_layout(
    title="Proporsi Jawaban",
    height=420,
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 3️⃣ MEAN SCORE PER QUESTION (SLEEK STYLE)
# =========================================================
mean_q = df_num.mean().sort_values(ascending=False)

fig3 = go.Figure()

fig3.add_bar(
    x=mean_q.index,
    y=mean_q.values,
    marker_color=COLORS["primary"],
    text=mean_q.round(2),
    textposition="outside"
)

fig3.update_layout(
    title="Rata-rata Skor per Pertanyaan",
    yaxis=dict(range=[0,5]),
    height=450,
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# 4️⃣ SENTIMENT CLEAN BAR
# =========================================================
def kategori(x):
    if x >= 4:
        return "Positif"
    elif x == 3:
        return "Netral"
    else:
        return "Negatif"

sentiment = series.apply(kategori).value_counts()

fig4 = go.Figure()

color_map = {
    "Positif": COLORS["positive"],
    "Netral": COLORS["neutral"],
    "Negatif": COLORS["negative"]
}

fig4.add_bar(
    x=sentiment.index,
    y=sentiment.values,
    marker_color=[color_map[i] for i in sentiment.index],
    text=sentiment.values,
    textposition="outside"
)

fig4.update_layout(
    title="Distribusi Sentimen Jawaban",
    height=400,
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# 5️⃣ GAUGE LUXURY STYLE
# =========================================================
fig5 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=mean_total,
    number={"suffix": " / 5"},
    gauge={
        "axis": {"range": [1,5]},
        "bar": {"color": COLORS["accent"]},
        "bgcolor": "white",
        "steps": [
            {"range": [1,2], "color": "#fee2e2"},
            {"range": [2,3], "color": "#fef3c7"},
            {"range": [3,4], "color": "#e0f2fe"},
            {"range": [4,5], "color": "#dcfce7"},
        ]
    }
))

fig5.update_layout(
    title="Indeks Kepuasan Keseluruhan",
    height=350
)

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# 6️⃣ HEATMAP CLEAN PROFESSIONAL
# =========================================================
corr = df_num.corr()

fig6 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues"
)

fig6.update_layout(
    title="Korelasi Antar Pertanyaan",
    height=500
)

st.plotly_chart(fig6, use_container_width=True)

# =========================================================
# AUTO INSIGHT SECTION
# =========================================================
best_q = mean_q.idxmax()
worst_q = mean_q.idxmin()

st.divider()
st.markdown("### 📌 Insight Otomatis")

st.success(f"Pertanyaan dengan skor tertinggi: **{best_q}** ({mean_q.max():.2f})")
st.error(f"Pertanyaan dengan skor terendah: **{worst_q}** ({mean_q.min():.2f})")
