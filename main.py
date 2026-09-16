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
    # genre에 여러 장르가 들어 있는 경우
    # "|" 또는 "/"를 구분자로 사용하고
    # 가장 앞에 있는 첫 번째 장르만 사용한다.
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
    "※ 여러 장르가 | 또는 /로 표시된 영화는 첫 번째 장르만 사용합니다."
)

# 장르별 영화 편수 계산
genre_count = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)

# --------------------------------------------------
# 도넛 그래프
# --------------------------------------------------
fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.5
)

fig.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
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
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 학생 해석 공간
# --------------------------------------------------
st.markdown("#### ✏️ 이 그래프로 알 수 있는 것")

st.text_area(
    "학생 해석",
    placeholder="그래프를 보고 알 수 있는 점을 한 문장으로 써 보세요.",
    height=100,
    label_visibility="collapsed"
)
```
