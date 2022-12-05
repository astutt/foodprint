
import streamlit as st
import PIL
import datetime
import torch
import pandas
import os

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

# Main page: static elements
st.title("Welcome to FoodPrint!") 
st.subheader("This application calculates the total carbon footprint of your foods in your grocery cart and provides food substitutions to reduce carbon footprint.")
opening_image = Image.open('gui_images/carbonemission.jpg')
st.image(opening_image, caption = None, width = 210, use_column_width = 210) 

# Sidebar inputs
welcome_image = Image.open('gui_images/welcome.jpg')
st.sidebar.image(welcome_image, caption = None, width = 145, use_column_width = 145) 

name = st.sidebar.text_input("What is your name?")
output_name = st.sidebar.write("Hi" + " " +  str(name) + "," +  " " + "welcome to FootPrint! We will help you calculate the carbon footprint of your food.")

st.sidebar.text_input("Please enter your location:")

today = datetime.date.today()
date = st.sidebar.write("Current Date: " + str(today)) 
str_date = str(today)

have_image = False
uploaded_image = st.sidebar.file_uploader("Upload an image of your grocery cart below:", type = ["png", "jpg", "jpeg"])
if uploaded_image is not None:
    food_image = Image.open(uploaded_image)
    filename = uploaded_image.name
    have_image = True

if ((have_image==True) & (st.sidebar.button("What's the carbon footprint of my shopping cart?"))):
    
    results = model(food_image)

    # save and display image
    results.save() 
    image_path = 'runs/detect/exp/image0.jpg'
    st.write("image path", image_path)
    result_image = Image.open(image_path)
    st.image(result_image)
    os.unlink(image_path)
    os.rmdir('runs/detect/exp')

    # type and number of foods
    table = results.pandas().xyxy[0]
    result_class = table['name']
    # ^^ right now is just a list of foods




st.write("Total carbon emissions of your grocery cart:  ")

st.write("Food Substitutions: ")

#month_data = datetime.datetime.strptime(str_date, "%Y-%m-%d")
#num_month = st.sidebar.write(month_data.month)

#Extracting the month (ex. current date: 2022-12-04 -> outputs: December )
month_gen= today.strftime("%B")







