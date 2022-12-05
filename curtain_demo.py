
import streamlit as st

import PIL.Image 

import datetime

from PIL import Image

from geopy.geocoders import Nominatim
from pprint import pprint
import time
import geocoder
import pandas as pd
import numpy as np

g = geocoder.ip('me')

app = Nominatim(user_agent="tutorial")

def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)

# define your coordinates
latitude = g.latlng[0]
longitude = g.latlng[1]
# get the address info
address = get_address_by_location(latitude, longitude)
# print all returned d
#print(address)
current_city = address['address']['city']

# Main page: Inputs
# shortcodes :apple::earth_americas::shopping_trolley:

st.title("Welcome to FoodPrint!:apple::shopping_trolley::earth_americas:")

st.subheader("This application calculates the total carbon footprint of your foods in your grocery cart and provides food substitutions to reduce carbon footprint.")


# sidebar inputs

image = Image.open(r"C:\Users\ltjth\Documents\GitHub\foodprint\image-removebg-preview (18).png")
st.sidebar.image(image, caption = None, width = 210, use_column_width = 210)

name = st.sidebar.text_input("What is your name?")

output_name = st.sidebar.write("Hi" + " " +  str(name) + "," +  " " + "welcome to FoodPrint! We will help you calculate the carbon footprint of your food.")
today = datetime.date.today()
st.sidebar.markdown('**Time and Location:**')
st.sidebar.write(current_city)
st.sidebar.markdown('**Current Date:**')
st.sidebar.write(str(today))
#st.sidebar.write(current_city)




#date = st.sidebar.write("Current Date: " + str(today))

#str_date = str(today)

my_image = st.sidebar.file_uploader("Upload an image of your grocery cart below:", type = ["png", "jpg", "jpeg"])

if my_image is not None:
    image = Image.open(my_image)
    st.sidebar.image(image)

if st.sidebar.button('Calculate total carbon emissions'):
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1)
    st.success('Thanks for doing your part!', icon="✅")
    tab1, tab2 = st.tabs(["Results", "Tips"])
    img2 = Image.open(r"C:\Users\ltjth\Documents\GitHub\foodprint\example pictures\example annotated_camila.png")
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            d = {'Item': ["Apples", "Oranges", "Carrots"], "Quantity": [1, 4, 2], "Emissions (kg)": [0.02, 1, .98]}
            #st.subheader("Estimated carbon emissions of your grocery cart: ")
            st.metric(label = "Co2 Emissions", value="2 kg Co2", delta="GOOD")
            st.write("We detected: ")
            df = pd.DataFrame(data=d)
            st.table(df)  # Same as st.write(df)
        with col2:
            st.image(img2)
    with tab2:
        st.header("Tips to Reduce Your Food's Carbon Emissions")
        st.subheader("- Eat produce that is in season")
        st.subheader("- Buy Local")
        st.subheader('- Decrease your red meat intake')
        st.markdown('[Learn More](https://ourworldindata.org/food-choice-vs-eating-local "Learn More")', unsafe_allow_html=False)

    # Step 1: Display the month name based on current date

    # month_data = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    # num_month = st.sidebar.write(month_data.month)

    # Extracting the month (ex. current date: 2022-12-04 -> outputs: December )
    month_gen = today.strftime("%B")

    # Step 2: Upload csv file to use vlookup on seasons vs. food

# Output Total Carbon Emissions
# Unit: kg C02








