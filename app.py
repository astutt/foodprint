import streamlit as st
import PIL
import datetime
import torch
import pandas
import os
import cv2
import PIL.Image
from PIL import Image
from geopy.geocoders import Nominatim
from pprint import pprint
import time
import geocoder
import pandas as pd
import numpy as np
apple_kg = 0.15
apple_co2 = 0.3
banana_kg = 0.12
banana_co2 = 0.8
citrus_kg = 0.14
citrus_co2 = 0.3
carrot_kg = 0.02
carrot_co2 = 0.3
broccoli_kg = 0.4
broccoli_co2 = 0.4
co2_total = 0
# ~~~~~~~~~~~~~~~~~~~~~~~ TO DO ~~~~~~~~~~~~~~~~~~~~~~~ #
#   display list of items (with cute emojis?) of how many of each thing you have

# lookup emissions values for each item
# display next to each item
# display total emissions

# cute reference statistics
# lookup what's out of season, add a little out of season list somewhere
# ^^ maybe with alternate veggies to buy
# have a whole other page displaying, by month, which things are in season

from PIL import Image 

# if 'image_count' not in st.session_state:
#     st.session_state.image_count = 0

# model params
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.25 # NMS confidence threshold
model.max_det = 100 # maximum number of detections per image


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

have_image = False
uploaded_image = st.sidebar.file_uploader("Upload an image of your grocery cart below:", type = ["png", "jpg", "jpeg"])
if uploaded_image is not None:
    food_image = Image.open(uploaded_image)
    filename = uploaded_image.name
    have_image = True

if ((have_image==True) & (st.sidebar.button("What's the carbon footprint of my shopping cart?"))):
    
    results = model(food_image)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1)
    st.success('Thanks for doing your part!', icon="✅")
    tab1, tab2 = st.tabs(["Results", "Tips"])
    img2 = Image.open(r"C:\Users\ltjth\Documents\GitHub\foodprint\example pictures\example annotated_camila.png")
    with tab1:
        # save and display image
        results.save()
        image_path = 'runs/detect/exp/image0.jpg'
        print(image_path)
        result_image = Image.open(image_path)
        col1, col2 = st.columns(2)
        with col1:
            # type and number of foods
            table = results.pandas().xyxy[0]
            print(table)
            big_list = table.name.values.tolist()
            print(big_list)
            detected = {':apple:Apples': 0, ':banana:Bananas': 0, ':tangerine:Oranges': 0, ':carrot:Carrots': 0, ':broccoli:Broccoli': 0}
            orange_count = 0
            apple_count = 0
            carrot_count = 0
            banana_count = 0
            broc_count = 0
            for x in big_list:
                if x == "orange":
                    orange_count += 1
                    detected[':tangerine:Oranges'] = orange_count
                elif x == "apple":
                    apple_count += 1
                    detected[':apple:Apples'] = apple_count
                elif x == "carrot":
                    carrot_count += 1
                    detected[':carrot:Carrots'] = carrot_count
                elif x == "banana":
                    banana_count += 1
                    detected[':banana:Bananas'] = banana_count
                elif x == "broccoli":
                    broc_count += 1
                    detected[':broccoli:Broccoli'] = broc_count
            print(detected)
            if detected[':apple:Apples'] != 0:
                apple_em = detected[':apple:Apples'] * apple_kg * apple_co2
                co2_total += apple_em
            elif detected[':banana:Bananas'] != 0:
                banana_em = detected[':banana:Bananas'] * banana_kg * banana_co2
                co2_total += banana_em
            elif detected[':tangerine:Oranges'] != 0:
                orange_em = detected[':tangerine:Oranges'] * citrus_kg * citrus_co2
                co2_total += orange_em
            elif detected[':carrot:Carrots'] != 0:
                carrot_em = detected[':carrot:Carrots'] * carrot_kg * carrot_co2
                co2_total += carrot_em
            elif detected[':broccoli:Broccoli'] != 0:
                broccoli_em = detected[':broccoli:Broccoli'] * broccoli_kg * broccoli_co2
                co2_total += broccoli_em
            print(co2_total)
            d = {'Item': ["Apples", "Oranges", "Carrots"], "Quantity": [1, 4, 2], "Emissions (kg)": [0.02, 1, .98]}
            # st.subheader("Estimated carbon emissions of your grocery cart: ")
            st.metric(label="kg Co2 Emissions", value=co2_total, delta="GOOD")
            st.write("We detected: ")
            for i in detected:
                if detected[i] != 0:
                    st.write(i, detected[i])
            #df = pd.DataFrame(data=d)
            #st.table(df)  # Same as st.write(df)
        with col2:
            st.image(result_image)
            os.unlink(image_path)
            os.rmdir('runs/detect/exp')


            #for index in table.iterrows():
            #    print(table['name'][index])
    with tab2:
        st.header("Tips to Reduce Your Food's Carbon Emissions")
        st.subheader("- Eat produce that is in season")
        st.subheader("- Buy Local")
        st.subheader('- Decrease your red meat intake')
        st.markdown('[Learn More](https://ourworldindata.org/food-choice-vs-eating-local "Learn More")',
                    unsafe_allow_html=False)

    #print(result_class)
    # ^^ right now is just a list of foods




#st.write("Total carbon emissions of your grocery cart:  ")

#st.write("Food Substitutions: ")

#month_data = datetime.datetime.strptime(str_date, "%Y-%m-%d")
#num_month = st.sidebar.write(month_data.month)

#Extracting the month (ex. current date: 2022-12-04 -> outputs: December )
month_gen= today.strftime("%B")







