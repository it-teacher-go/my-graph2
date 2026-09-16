```python
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/"
    "kobis_movies.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # genre에 여러 장르가 |로 구분되어 있는 경우
    # 반드시 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|", regex=False)
        .str[0]
        .str.strip()
    )

    return df


df = load_data()

# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
with st.expander("데이터 보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ==================================================
# ① 장르별 영화 편수
# ==================================================
st.subheader("① 장르별 영화 편수")

st.caption(
    "※ 여러 장르가 세로막대(|)로 표시된 영화는 첫 번째 장르만 사용합니다."
)

genre_count = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.5,
)

fig.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    ),
)

fig.update_layout(
    height=520,
    margin=dict(t=30, b=20, l=20, r=20),
    legend_title_text="장르",
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 학생 해석 공간
# --------------------------------------------------
st.markdown("#### ✏️ 이 그래프로 알 수 있는 것")

st.text_area(
    "학생 해석",
    placeholder="그래프를 보고 알 수 있는 점을 한 문장으로 써 보세요.",
    height=100,
    label_visibility="collapsed",
    key="interpretation_1",
)

st.divider()

# ==================================================
# ② 다음 그래프 자리
# ==================================================
st.subheader("② 다음 그래프")

st.info("다음 그래프를 추가할 자리입니다.")

st.markdown("#### ✏️ 이 그래프로 알 수 있는 것")

st.text_area(
    "학생 해석",
    placeholder="그래프를 보고 알 수 있는 점을 한 문장으로 써 보세요.",
    height=100,
    label_visibility="collapsed",
    key="interpretation_2",
)
```
