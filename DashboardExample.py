import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Volvo Price Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

df = pd.read_csv("VolvoAllUsedTrend.csv")
df.drop(df.tail(1).index,inplace=True)


with st.sidebar:
    st.title('🚕 Volvo Price Dashboard')
    date_list = list(df.Date.unique())[::-1]
    selected_date = st.selectbox("Select Date", date_list, index=len(date_list)-1)
    df_selected_date = df[df.Date == selected_date]
    df_selected_date_sorted = df_selected_date.sort_values(by="Price", ascending=False)
    color_theme_list = ['blues','cividis','greens']
    select_color_theme = st.selectbox("Select a color theme", color_theme_list)