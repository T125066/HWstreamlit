import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# ページ設定
# =====================
st.set_page_config(page_title="人口分析ダッシュボード", layout="wide")
st.title("🏙 都道府県別 人口分析ダッシュボード")

# CSV読み込み
df = pd.read_csv("c01.csv", encoding="cp932")

# 数値変換（超重要）
for col in ["人口（総数）", "人口（男）", "人口（女）"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =====================
# サイドバー
# =====================
st.sidebar.header("分析条件")

selected_prefs = st.sidebar.multiselect(
    "都道府県",
    df["都道府県名"].unique(),
    default=[df["都道府県名"].unique()[0]]
)

selected_year = st.sidebar.selectbox(
    "西暦（年）",
    sorted(df["西暦（年）"].unique())
)

# =====================
# データ絞り込み
# =====================
df_filtered = df[
    (df["都道府県名"].isin(selected_prefs)) &
    (df["西暦（年）"] == selected_year)
]

# =====================
# KPI
# =====================
total_pop = df_filtered["人口（総数）"].sum()
male_pop = df_filtered["人口（男）"].sum()
female_pop = df_filtered["人口（女）"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("👥 総人口", f"{total_pop:,}")
c2.metric("👨 男性人口", f"{male_pop:,}")
c3.metric("👩 女性人口", f"{female_pop:,}")

# =====================
# タブUI
# =====================
tab1, tab2 = st.tabs(["📋 データ表", "📊 グラフ"])

# ---- 表 ----
with tab1:
    st.dataframe(df_filtered, use_container_width=True)

# ---- グラフ ----
with tab2:
    st.subheader("都道府県別 人口（男女）")

    df_long = df_filtered.melt(
        id_vars=["都道府県名"],
        value_vars=["人口（男）", "人口（女）"],
        var_name="性別",
        value_name="人口"
    )

    fig = px.bar(
        df_long,
        x="都道府県名",
        y="人口",
        color="性別",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# 人口推移（複数年）
# =====================
st.subheader("📈 人口推移（総数）")

df_trend = df[df["都道府県名"].isin(selected_prefs)]

fig2 = px.line(
    df_trend,
    x="西暦（年）",
    y="人口（総数）",
    color="都道府県名"
)

st.plotly_chart(fig2, use_container_width=True)
