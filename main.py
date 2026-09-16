import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 영화 가운데, 이 기간에 개봉한 216편의 데이터를 살펴봅니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, dtype={"movieCd": str, "openDt": str})

    # 개봉일: 여덟 자리 숫자를 날짜로 변환
    df["openDt"] = (
        df["openDt"]
        .astype(str)
        .str.extract(r"(\d{8})", expand=False)
    )
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 여러 장르가 세로막대(|)로 연결된 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
        .replace("", "미상")
    )

    # 숫자형 열 정리
    numeric_cols = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.code(str(e))
    st.stop()

# ---------------------------
# 그래프 1. 장르별 영화 편수
# ---------------------------
st.subheader("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("genre")
    .reset_index(name="count")
)

total = genre_counts["count"].sum()
genre_counts["ratio"] = genre_counts["count"] / total * 100

fig = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.55,
    custom_data=["count", "ratio"],
)

fig.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{customdata[0]}편<br>비율: %{customdata[1]:.1f}%<extra></extra>",
    textposition="inside",
    textinfo="percent",
)

fig.update_layout(
    showlegend=True,
    legend_title_text="장르",
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것**")
    st.text_input(
        "내용을 직접 입력하세요.",
        key="interpretation_1",
        placeholder="예: 이 기간에는 ○○ 장르 영화가 가장 많이 포함되어 있다.",
        label_visibility="collapsed",
    )

st.divider()

st.caption("※ 장르가 여러 개 표시된 영화는 첫 번째 장르만 집계했습니다.")
