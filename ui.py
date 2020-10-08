import streamlit as st
import pandas as pd
import requests
import os
from model import train, predict

# interact with FastAPI endpoint
port = int(os.environ.get("PORT", 5000))
url = 'http://0.0.0.0:' + str(port)

endpoint = '/predict'

df = pd.read_csv('data\listings.csv')

st.sidebar.markdown(
"""
### About
This project aims to combine a **web app and an API** using **Streamlit and FastAPI**.

The data comes from Murray Cox project [Inside Airbnb](https://insideairbnb.com/get-the-data.htm)
and was goten the 13th of September, 2020.
Source code can be found at [GitHub](https://github.com/Sampayob).

**Author**: Sergio Sampayo
""")

st.title("Madrid 🏠 AirBnb")
st.subheader("Get your house assessed for Aibnb")

neighbourhood_group_list = sorted(df['neighbourhood_group'].unique())
neighbourhood_group = st.selectbox('Neighbourhood group', neighbourhood_group_list)

neighbourhood_list = sorted(df[df['neighbourhood_group'] == neighbourhood_group]['neighbourhood'].unique())
neighbourhood = st.selectbox('Neighbourhood',neighbourhood_list)

room_type_list = sorted(df[df['neighbourhood'] == neighbourhood]['room_type'].unique())
room_type = st.selectbox('Room type', room_type_list)

minimum_nights_list = sorted(df['minimum_nights'].unique())
minimum_nights = st.selectbox('Minimum nights', minimum_nights_list)

if st.button("Submit"):

    if neighbourhood_group == None or neighbourhood == None or room_type == None or minimum_nights == None:
        st.write("Fill all the options")

    r = requests.post(url+endpoint,json={'param1': neighbourhood_group, 'param2': neighbourhood, 'param3': room_type, 'param4': int(minimum_nights)})

    train()
    prediction = predict(neighbourhood_group, neighbourhood, room_type, minimum_nights)
    st.info(f"**{prediction}€** per night should be charged")
