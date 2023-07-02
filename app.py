import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import streamlit_toggle as tog

from utils import *

st.set_page_config(
    page_title="Real-Time User Survey Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Real-Time User Survey Dashboard")
st.sidebar.title("원하는 필터를 적용하세요.")

# load_data
df = load_data()

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
selected_df = selected_df[selected_df["커피선호종류"] == selected_coffee]

filter_coffe_columns = filter_coffee(selected_df, selected_coffee)
selected_df = selected_df[filter_coffe_columns]

st.dataframe(selected_df)
st.text(f"데이터프레임 크기 : {selected_df.shape}")
