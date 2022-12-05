
import streamlit as st

import PIL.Image 

import datetime

from PIL import Image 

# Main page: Inputs

st.title("Welcome to FoodPrint!") 

st.subheader("This application calculates the total carbon footprint of your foods in your grocery cart and provides food substitutions to reduce carbon footprint.")

image = Image.open('carbonemission.jpg')

st.image(image, caption = None, width = 210, use_column_width = 210) 



# sidebar inputs

image_two = Image.open('welcome.jpg')

st.sidebar.image(image_two, caption = None, width = 145, use_column_width = 145) 

name = st.sidebar.text_input("What is your name?")

output_name = st.sidebar.write("Hi" + " " +  str(name) + "," +  " " + "welcome to FootPrint! We will help you calculate the carbon footprint of your food.")

st.sidebar.text_input("Please enter your location:")

today = datetime.date.today()

date = st.sidebar.write("Current Date: " + str(today)) 

str_date = str(today)

my_image = st.sidebar.file_uploader("Upload an image of your grocery cart below:", type = ["png", "jpg", "jpeg"])

if my_image is not None:
    
    image = Image.open(my_image)

st.sidebar.button('Calculate total carbon emissions')



# Output Total Carbon Emissions
# Unit: kg C02

st.write("Total carbon emissions of your grocery cart:  ")

st.write("Food Substitutions: ")

# Step 1: Display the month name based on current date

#month_data = datetime.datetime.strptime(str_date, "%Y-%m-%d")
#num_month = st.sidebar.write(month_data.month)

#Extracting the month (ex. current date: 2022-12-04 -> outputs: December )
month_gen= today.strftime("%B")


# Step 2: Upload csv file to use vlookup on seasons vs. food







