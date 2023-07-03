import numpy as np
import pandas as pd

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["recoreconi@angular-glyph-351208.iam.gserviceaccount.com"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

conn = connect(credentials=credentials)


def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def EDA(rows) -> pd.DataFrame:

    df = pd.DataFrame(rows).iloc[:, 3:]

    rename_columns = [
    '성별',
    '나이',
    '직업',
    '커피음용빈도',
    '커피선호종류',
    '원두_선호상품',
    '원두_선호분쇄정도',
    '원두_다른커피선호여부',
    '캡슐_선호상품',
    '캡슐_머신호환캡슐',
    '캡슐_다른커피선호여부',
    '드립백_선호상품',
    '드립백_다른커피선호여부',
    '인스턴트_선호상품',
    '인스턴트_다른커피선호여부',
    '커피이해도',
    '커피구매중요요소',
    '커피선호중요요소',
    '선호_향',
    '선호_산미',
    '선호_단맛',
    '선호_바디감',
    '기존사이트취향추천정당여부',
    '입문자커피취향탐색난항여부',
    '추천사이트사용여부',
    '추천사이트사용여부_이유'
    ]

    df = df.rename(columns = dict(zip(df.columns, rename_columns)))

    return df


def load_sheets() -> pd.DataFrame:
    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')
    df = EDA(rows)
    return df


@st.cache_data
def load_data():
    """
    추후 구글시트(gspread) 와 연동 필요
    """
    df = pd.read_csv("./data/0702_survey.csv")

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
