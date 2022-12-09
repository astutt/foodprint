import streamlit as st
import datetime
import torch
import os
import time
import geocoder
import pandas as pd
import numpy as np

from PIL import Image
from geopy.geocoders import Nominatim
from pprint import pprint


# variables for emissions calculator
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
orange_count = 0
apple_count = 0
carrot_count = 0
banana_count = 0
broc_count = 0

# model params
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.25 # NMS confidence threshold
model.max_det = 100 # maximum number of detections per image

#~~~~~~~~~~~~~~~~~ auto city detection~~~~~~~~~~~~~~~~~~~~~#
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
# detect city from coordinates
latitude = g.latlng[0]
longitude = g.latlng[1]
address = get_address_by_location(latitude, longitude)
current_city = address['address']['city']

#~~~~~~~~~~~~~~~~~ GUI ~~~~~~~~~~~~~~~~~~~~~#
# Main page
st.title("Welcome to FoodPrint!:apple::shopping_trolley::earth_americas:")
st.subheader("This application calculates the total carbon footprint of the food in your grocery cart and compares it to other real world carbon emissions. Keep track of your carbon footprint with Foodprint!")

# Sidebar
image = Image.open(r"./gui_images/logo.png")
st.sidebar.image(image, caption = None, width = 210, use_column_width = 210)
name = st.sidebar.text_input("What is your name?")
if name:
    output_name = st.sidebar.write("Hi " + str(name) + ", welcome to FoodPrint! We will help you calculate the carbon footprint of your food.")

# Output current time and location
today = datetime.date.today()
st.sidebar.markdown('**Time and Location:**')
st.sidebar.write(current_city)
st.sidebar.markdown('**Current Date:**')
st.sidebar.write(str(today))

# ML Stuff
have_image = False
uploaded_image = st.sidebar.file_uploader("Upload an image of your grocery cart below:", type = ["png", "jpg", "jpeg"])
if uploaded_image is not None:
    food_image = Image.open(uploaded_image)
    filename = uploaded_image.name
    have_image = True

# Run model, compute emissions, display on GUI
if ((have_image==True) & (st.sidebar.button("What's the carbon footprint of my shopping cart?"))):
    
    results = model(food_image)
    # progress bar that does absolutely nothing but look cool
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1)
    st.success('Thanks for doing your part!', icon="✅")

    # split into two tabular sections
    tab1, tab2 = st.tabs(["Results", "Tips"])
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
            results_list = table.name.values.tolist()
            print(results_list)

            # emissions calculator stuff
            # dictionary that will have the amount of each item
            # the stuff in semicolons are emojis :)
            detected = {':apple:Apples': 0, ':banana:Bananas': 0, ':tangerine:Oranges': 0, ':carrot:Carrots': 0, ':broccoli:Broccoli': 0}

            # counting each item from the results list that yolo spits out
            for x in results_list:
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

            # if item is detected and has nonzero items in the image, do math
            # total per item = quantity*item avg weight (kgItem)*co2 emissions per item(kgCo2/kgItem)
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

            # display emissions as a metric because it looks cool
            # the delta is just a dummy rn, can be made to indicate something
            st.metric(label="kg Co2 Emissions", value=co2_total, delta="GOOD")
            # compare your emissions to something in the real world! Aka driving a car 1 mile = 0.034 kg of carbon emissions
            drive = round((co2_total/0.034), 2)
            st.write("This is equal to driving :car: ", str(drive), "miles")
            
            st.write("We detected: ")
            # displays nonzero keys, thus displays items detected
            for i in detected:
                if detected[i] != 0:
                    st.write(i, detected[i])
        with col2:
            # displays image with bounding boxes from yolo
            st.image(result_image)
            os.unlink(image_path)
            os.rmdir('runs/detect/exp')

    with tab2:
        # info about reducing your emissions
        # this can also include the seasons table, this stuff is just kinda placeholder for now
        st.header("Tips to Reduce Your Food's Carbon Emissions")
        st.subheader("- Eat produce that is in season")
        st.subheader("- Buy Local")
        st.subheader('- Decrease your red meat intake')
        st.markdown('[Learn More](https://ourworldindata.org/food-choice-vs-eating-local "Learn More")',
                    unsafe_allow_html=False)

month_gen= today.strftime("%B")







