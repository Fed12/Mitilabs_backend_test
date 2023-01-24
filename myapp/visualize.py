"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import boto3
from .settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

def load_data(first_bucket_name, first_file_name):
    s3_resource = boto3.resource('s3')
    # first_bucket = s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME)
    # first_bucket_name = 'havtrackwatchappmain42b95d92f7eb4d85aa3b21a88ae125522-dev'
    # first_file_name = 'Cachedtest_file_(1).xls'
    first_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name)

    df = first_object
    print(' type(df)')
    print(type(df), ' type(df)')
    print(' type(df)')
    print('s3://' + first_bucket_name + '/' + first_file_name)

    df = pd.read_excel('s3://' + first_bucket_name + '/' + first_file_name)
    # df = pd.read_excel(first_object, engine='xlrd')
    df = df.rename(columns={'Motion Sensor': 'date', 'Unnamed: 1': "sensor"})
    df = df.drop(columns={'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'})
    # lowercase = lambda x: str(x).lower()
    # df.rename(lowercase, axis='columns', inplace=True)

    import datetime as dt
    df['date'] = pd.to_datetime(df['date'])
    df['YW'] = df['date'].dt.year * 100 + df['date'].dt.isocalendar().week
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna()

    return df


#Ladder Score Slider Filter
def sidebar_filter(df):
    score = st.sidebar.slider('Select min X', min_value=0.00003, max_value=20.0)  # Getting the input.
    df = df[df['X'] >= score]  # Filtering the dataframe.
    score = st.sidebar.slider('Select min Y', min_value=0.00003, max_value=20.0)  # Getting the input.
    df = df[df['Y'] >= score]  # Filtering the dataframe.
    score = st.sidebar.slider('Select min Z', min_value=0.00003, max_value=20.0)  # Getting the input.
    df = df[df['Z'] >= score]  # Filtering the dataframe.
    st.write(df)


def plot(df):
    import plotly.express as px
    import seaborn as sns
    # Scatter Chart
    # fig = px.scatter(
    #     df,
    #     x="YW",
    #     y="Y",
    #     # size="Z",
    #     color="Z",
    #     # hover_name="Z",
    #     size_max=10
    # )
    #
    # st.write(fig)

    # Bar Chart, you can write in this way too
    st.write(px.bar(df, y='Y', x='YW'))


# LINE CHART
def line(df):

    st.line_chart(data=df, x='YW', y='sensor', width=300, height=300, use_container_width=True)

#
# df = load_data("Cached.xls")
# print(df.dtypes)
# sidebar_filter(df)
# plot(df)
# # print(df.date)
#
# #TITLES
# st.title("Cached data")
# st.sidebar.title("Sidebar Slider Filter")






