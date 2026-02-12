import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Executive Survey Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CUSTOM CSS (HD PROFESSIONAL LOOK)
# =====================================================
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}
.metric-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
}
.big-title {
    font-size: 34px;
    font-weight: 700;
}
.subtitle {
    color: gray;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx", engine="openpyxl")

df = load_data()
df_num = df.select_dtypes(include="number")

# =====================================================
# HEADER
# =====================================================
st.markdown('<div class="big-title">📊 Executive Survey Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">High-Definition Professional Dashboard</div>', unsafe_allow_html=True)

# =====================================================
# KPI SECTION
# =====================================================
mean_total = df_num.mean().mean()
total_responden = len(df)
best_q = df_num.mean().idxmax()
worst_q = df_num.mean().idxmin()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Responden", total_responden)
col2.metric("Rata-rata Skor", f"{mean_total:.2f} / 5")
col3.metric("Pertanyaan Terbaik", best_q)
col4.metric("Perlu Perbaikan", worst_q)

st.markdown("---")

# =====================================================
# DISTRIBUSI KESELURUHAN
# =====================================================
all_values = df_num.values.flatten()
series = pd.Series(all_values)
dist = series.value_counts().sort_index()

fig1 = go.Figure()

fig1.add_bar(
    x=dist.index,
    y=dist.values,
    marker=dict(
        color="#2563eb",
        line=dict(width=0)
    ),
    text=dist.values,
    textposition="outside"
)

fig1.update_layout(
    title="Distribusi Jawaban Keseluruhan",
    height=550,
    plot_bgcolor="white",
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# DONUT HD
# =====================================================
fig2 = go.Figure(go.Pie(
    labels=dist.index,
    values=dist.values,
    hole=0.7,
    textinfo="percent",
    marker=dict(
        colors=["#1e3a8a","#2563eb","#3b82f6","#60a5fa","#93c5fd"]
    )
))

fig2.update_layout(
    title="Proporsi Jawaban",
    height=550,
    showlegend=True
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# RATA-RATA PER PERTANYAAN
# =====================================================
mean_q = df_num.mean().sort_values(ascending=False)

fig3 = go.Figure()

fig3.add_bar(
    x=mean_q.index,
    y=mean_q.values,
    marker_color="#111827",
    text=mean_q.round(2),
    textposition="outside"
)

fig3.update_layout(
    title="Rata-rata Skor per Pertanyaan",
    yaxis=dict(range=[0,5]),
    height=600,
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# SENTIMENT DISTRIBUTION
# =====================================================
def kategori(x):
    if x >= 4:
        return "Positif"
    elif x == 3:
        return "Netral"
    else:
        return "Negatif"

sentiment = series.apply(kategori).value_counts()

colors = {
    "Positif": "#22c55e",
    "Netral": "#f59e0b",
    "Negatif": "#ef4444"
}

fig4 = go.Figure()

fig4.add_bar(
    x=sentiment.index,
    y=sentiment.values,
    marker_color=[colors[i] for i in sentiment.index],
    text=sentiment.values,
    textposition="outside"
)

fig4.update_layout(
    title="Distribusi Sentimen Jawaban",
    height=500,
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# GAUGE ULTRA CLEAN
# =====================================================
fig5 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=mean_total,
    number={"suffix": " / 5"},
    gauge={
        "axis": {"range": [1,5]},
        "bar": {"color": "#2563eb"},
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
    height=450
)

st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# HEATMAP HD
# =====================================================
corr = df_num.corr()

fig6 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues",
    aspect="auto"
)

fig6.update_layout(
    title="Korelasi Antar Pertanyaan",
    height=650
)

st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# AUTO INSIGHT BOX
# =====================================================
st.markdown("---")
st.markdown("### 📌 Executive Insight")

st.info(
    f"""
    • Skor rata-rata keseluruhan berada pada **{mean_total:.2f}** dari skala 5.  
    • Pertanyaan dengan performa terbaik adalah **{best_q}**.  
    • Pertanyaan yang perlu perhatian adalah **{worst_q}**.  
    • Mayoritas respon menunjukkan kecenderungan positif terhadap survei.
    """
)
