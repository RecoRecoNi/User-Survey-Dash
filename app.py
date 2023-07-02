import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

from matplotlib import rc

import streamlit as st
import streamlit_toggle as tog

from utils import *

import matplotlib.font_manager as fm

# rc("font", family="AppleGothic")
# plt.rcParams["axes.unicode_minus"] = False


st.set_page_config(
    page_title="Real-Time User Survey Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Real-Time User Survey Dashboard")
st.sidebar.title("원하는 필터를 적용하세요.")

fontRegistered()
# fontNames = [f.name for f in fm.fontManager.ttflist]
fontNames = ["NanumGothic", "AppleGothic"]
fontname = st.sidebar.selectbox("폰트 선택 (나눔 고딕 권장)", unique(fontNames))

plt.rc("font", family=fontname)

# load_data
df = load_data()
df = preprocess(df)


# check box
selected_gender = st.sidebar.multiselect("확인하고 싶은 성별을 선택하세요. (복수선택가능)", pd.unique(df["성별"]), default=["남성", "여성"])
selected_age = st.sidebar.multiselect(
    "확인하고 싶은 나이대를 선택하세요. (복수선택가능)",
    pd.unique(df["나이"]),
    default=["10대", "20대", "30대", "40대", "50대 이상"],
)
selected_job = st.sidebar.multiselect(
    "확인하고 싶은 직업을 선택하세요. (복수선택가능)",
    pd.unique(df["직업"]),
    default=pd.unique(df["직업"]),
)
selected_coffee = st.sidebar.selectbox(
    "확인하고 싶은 커피 종류를 선택하세요.",
    pd.unique(df["커피선호종류"]),
)

selected_df = df[df["성별"].isin(selected_gender)]
selected_df = selected_df[selected_df["나이"].isin(selected_age)]
selected_df = selected_df[selected_df["직업"].isin(selected_job)]


selected_coffee_df = selected_df[selected_df["커피선호종류"] == selected_coffee]
filter_coffe_columns = filter_coffee(selected_coffee_df, selected_coffee)
selected_coffee_df = selected_coffee_df[filter_coffe_columns]

if st.sidebar.checkbox("메타 데이터 확인"):
    st.subheader("메타 데이터")
    st.text(f"데이터프레임 크기 : {selected_df.shape}")
    st.dataframe(selected_df)

if st.sidebar.checkbox("커피 선호종류에 따른 데이터 확인"):
    st.subheader("커피 선호종류에 따른 데이터")
    st.text(f"데이터프레임 크기 : {selected_coffee_df.shape}")
    st.dataframe(selected_coffee_df)


st.subheader("유저 프로필")
plot_user_profile(selected_coffee_df)
st.subheader("유저 별 커피 프로필")
plot_user_coffee_info(selected_coffee_df)

# gender group
gender_groups = selected_df["성별"].unique()
gender_acidity = [
    selected_df.loc[selected_df["성별"] == gender_groups[0], "선호_산미"].dropna().values,
    selected_df.loc[selected_df["성별"] == gender_groups[1], "선호_산미"].dropna().values,
]

st.subheader("성별에 따른 선호 산미")
st.bar_chart(selected_df.groupby("성별")["선호_산미"].value_counts().unstack(), use_container_width=True)

# fig = ff.create_distplot(gender_acidity, gender_groups)
# st.plotly_chart(fig, use_container_width=True)
