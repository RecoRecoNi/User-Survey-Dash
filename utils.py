import numpy as np
import pandas as pd

import streamlit as st


@st.cache_data
def load_data():
    """
    추후 구글시트(gspread) 와 연동 필요
    """
    df = pd.read_csv("./data/example_survey.csv")

    return df


def filter_coffee(df: pd.DataFrame, prefer_coffee: str):
    basic_columns = [
        "성별",
        "나이",
        "직업",
        "커피음용빈도",
        "커피선호종류",
        "커피이해도",
        "커피구매중요요소",
        "커피선호중요요소",
        "선호_향",
        "선호_산미",
        "선호_단맛",
        "선호_바디감",
        "기존사이트취향추천정당여부",
        "입문자커피취향탐색난항여부",
        "추천사이트사용여부",
        "추천사이트사용여부_이유",
    ]

    prefer_coffee = prefer_coffee[:2]

    filter_cols = []

    for col in df.columns.tolist():
        if prefer_coffee in col:
            filter_cols.append(col)

    columns = filter_cols + basic_columns

    return columns
