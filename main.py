```python
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 페이지 설정
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
# 데이터 주소
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/"
    "kobis_movies.csv"
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # ----------------------------------------------
    # 장르 전처리
    # ----------------------------------------------
    # "|" 또는 "/"가 여러 장르의 구분자로 사용된 경우
    # 첫 번째 장르만 사용한다.
    #
    # 예:
    # "공포(호러)|멜로/로맨스" → "공포(호러)"
    # "액션/어드벤처" → "액션"
    # "드라마|코미디" → "드라마"
    # ----------------------------------------------
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.replace("/", "|", regex=False)
        .str.split("|", regex=False)
        .str[0]
        .str.strip()
    )

    # 빈 장르는 기타로 처리
    df.loc[df["genre"] == "", "genre"] = "기타"

    # 총 관객 수를 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    ).fillna(0)

    return df


df = load_data()


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
with st.expander("데이터 보기"):
    st.dataframe(df, use_container_width=True)

st.divider()


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================
st.header("1. 장르별 영화 편수")

st.caption(
    "※ 여러 장르가 | 또는 /로 표시된 영화는 첫 번째 장르만 사용합니다."
)

genre_count = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)


# --------------------------------------------------
# 도넛 그래프
# --------------------------------------------------
fig1 = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.5
)

fig1.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    height=520,
    margin=dict(
        t=30,
        b=20,
        l=20,
        r=20
    ),
    legend_title_text="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


st.divider()


# ==================================================
# 그래프 2. 장르 안의 영화 (트리맵)
# ==================================================
st.header("2. 장르 안의 영화 (트리맵)")

st.caption(
    "※ 칸의 크기는 총 관객 수를 나타냅니다. "
    "마우스를 올리면 영화명과 총 관객 수를 확인할 수 있습니다."
)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    ),
    textinfo="label"
)

fig2.update_layout(
    height=650,
    margin=dict(
        t=30,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


st.divider()


# ==================================================
# 그래프 3. 총 관객의 분포 (히스토그램)
# ==================================================
st.header("3. 총 관객의 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=40
)

fig3.update_layout(
    height=500,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

under_1m = (
    df["total_audi"] < 1_000_000
).sum()

best = df.loc[
    df["total_audi"].idxmax()
]

st.write(
    f"216편 가운데 {under_1m}편이 100만 명 미만입니다. "
    f"가장 많이 본 영화는 "
    f"{best['movieNm']}({best['total_audi']:,}명)입니다."
)

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)
```
