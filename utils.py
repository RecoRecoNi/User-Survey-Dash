import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st


@st.cache_data
def load_data():
    """
    추후 구글시트(gspread) 와 연동 필요
    """
    df = pd.read_csv("./data/example_survey.csv")

    return df


# 한글폰트 적용
import os
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm


@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + "/customFonts"]
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def unique(list):
    x = np.array(list)
    return np.unique(x)


def preprocess(df):
    df = df.replace("캡슐 커피(네스프레소, 일리 등)", "캡슐 커피")

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


import matplotlib.colors as mcolors
import colorsys


def set_hls(c, dh=0, dl=0, ds=0, dalpha=0):
    """
    c : (array -like, str) color in RGB space
    dh : (float) change in Hue
        default = 0
    dl : (float) change in Lightness
        default = 0
    ds : (float) change in Saturation
        default = 0
    """
    # 입력된 color를 RGBA numpy array로 변환
    c_rgba = mcolors.to_rgba(c)

    # RGB와 alpha 분리
    c_rgb = c_rgba[:3]
    alpha = c_rgba[3]

    # RGB 색공간을 HLS 색공간으로 변환 후 입력된 변화 적용
    c_hls = colorsys.rgb_to_hls(*c_rgb)
    h = c_hls[0] + dh
    l = max(min(c_hls[1] + dl, 1), 0)  # 0~1 범위를 넘지 않도록 제어
    s = max(min(c_hls[2] + ds, 1), 0)  # 0~1 범위를 넘지 않도록 제어

    # HLS 색공간에서 변경된 색을 RGB 색공간으로 변환
    c_rgb_new = colorsys.hls_to_rgb(h, l, s)
    alpha = max(min(alpha + dalpha, 1), 0)  # 0~1 범위를 넘지 않도록 제어

    return np.append(c_rgb_new, alpha)  # alpha 추가하여 retur


def plot_bar(df, col):
    fig, ax = plt.subplots(figsize=(5, 3), constrained_layout=True)

    sns.countplot(y=col, data=df, ax=ax)

    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.set(xticks=[], xlabel="", ylabel="")
    ax.set_title(f"count {col}", color="gray", fontweight="bold")

    for i, p in enumerate(ax.patches):
        x, width = p.get_x(), p.get_width()
        if i < 2:
            fc = set_hls(p.get_fc(), dl=0.4, ds=-0.3)
            c = "gray"
        else:
            fc = set_hls(p.get_fc(), ds=0.2)
            c = "w"
        p.set_fc(fc)
        # c = "gray" if i < 2 else "w"
        ax.text(width - 3, i, f"{width}", c=c, ha="right", va="center", fontweight="bold")

    st.pyplot(fig)


def plot_user_profile(df):
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(8, 2), constrained_layout=True)
    axs = axes.ravel()
    cols = ["성별", "나이", "직업"]

    for idx, ax in enumerate(axs):
        sns.countplot(y=cols[idx], data=df, ax=ax)

        ax.spines[["top", "right", "bottom"]].set_visible(False)
        ax.set(xticks=[], xlabel="", ylabel="")
        ax.set_title(f"percent of {cols[idx]}", color="gray", fontweight="bold")

        total_len = len(df)
        for i, p in enumerate(ax.patches):
            x, width = p.get_x(), p.get_width()
            fc = set_hls(p.get_fc(), dl=0.2, ds=-0.1)
            c = "black"
            p.set_fc(fc)
            percent = round(round(width / total_len, 2) * 100)

            if percent >= 15:
                text_loc = width - 2
            else:
                text_loc = width + 20
            ax.text(
                text_loc,
                i,
                f"{percent}%",
                c=c,
                ha="right",
                va="center",
                fontweight="bold",
                fontsize=8,
            )

    st.pyplot(fig)


def plot_user_coffee_info(df):
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(8, 2), constrained_layout=True)
    axs = axes.ravel()
    cols = ["커피음용빈도", "커피선호종류"]

    for idx, ax in enumerate(axs):
        sns.countplot(y=cols[idx], data=df, ax=ax)

        ax.spines[["top", "right", "bottom"]].set_visible(False)
        ax.set(xticks=[], xlabel="", ylabel="")
        ax.set_title(f"percent of {cols[idx]}", color="gray", fontweight="bold")

        total_len = len(df)
        for i, p in enumerate(ax.patches):
            x, width = p.get_x(), p.get_width()
            fc = set_hls(p.get_fc(), dl=0.2, ds=-0.1)
            c = "black"
            p.set_fc(fc)
            percent = round(round(width / total_len, 2) * 100)

            if percent >= 10:
                text_loc = width - 2
            else:
                text_loc = width + 8
            ax.text(
                text_loc,
                i,
                f"{percent}%",
                c=c,
                ha="right",
                va="center",
                fontweight="bold",
                fontsize=8,
            )

    st.pyplot(fig)


# def plot_user_coffee_info(df):
