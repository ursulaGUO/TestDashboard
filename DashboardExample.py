import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Volvo Price Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")



###########################
# Prepping the dataframe
###########################
df = pd.read_csv("VolvoAllUsedTrend.csv")

# Dropping last line which contains irrelevant data
df.drop(df.tail(1).index,inplace=True) 
df.drop(columns = ["Avg Price","Last 30 Days", "Last 90 Days", "YoY Change"], inplace=True)

# Extracting year out of date
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df_new = pd.DataFrame()

# Creating two seperate columns with different prices
df["Volvo Price"] = df["Price"].where(df["Car Type"] == "Volvo")
df["Average Market Price"] = df["Price"].where(df["Car Type"] == "CarGurus Index")
df_volvo = df.dropna(subset = ['Volvo Price'])
df_volvo.drop(columns = ["Average Market Price"],inplace=True)
df_market = df.dropna(subset = ["Average Market Price"])
df_market.drop(columns = ["Volvo Price"],inplace=True)
df = pd.merge(df_volvo, df_market[["Date","Average Market Price"]], on="Date")
df.drop(columns = ["Car Type","Price"], inplace=True)



###########################
# Sidebar selection options
###########################
# Include a start date and an end date

with st.sidebar:
    st.title('🚕 Volvo Price Dashboard')
    year_list = list(df.Year.unique())[::] # in ascending order
    selected_start_year = st.selectbox("Select Start Year", year_list, index=len(year_list)-1)
    end_year_list = list(df.Year.where(df["Year"] >= selected_start_year).unique())
    selected_end_year = st.selectbox("Select End Year", end_year_list, index=len(end_year_list)-1)
    df_selected_years = df[(df.Year >= selected_start_year) & (df.Year <= selected_end_year)]
    df_selected_years_sorted = df_selected_years.sort_values(by="Price", ascending=False)
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


# Writing paragraphs on page
st.write("""
         # Volvo Sales Trend
         Click to see how Volvo's price has changed over time in the second hand market""")

df_selected_years

# Plotting a line chart on page
st.line_chart(data=df_selected_years, x='Date', y=["Volvo Price", "Average Market Price"])
