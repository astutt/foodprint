
import streamlit as st
import PIL.Image 
import datetime

from PIL import Image 

# Main page: static elements
st.title("Welcome to FoodPrint!") 
st.subheader("This application calculates the total carbon footprint of your foods in your grocery cart and provides food substitutions to reduce carbon footprint.")
opening_image = Image.open('carbonemission.jpg')
st.image(opening_image, caption = None, width = 210, use_column_width = 210) 

# Sidebar inputs
welcome_image = Image.open('welcome.jpg')
st.sidebar.image(welcome_image, caption = None, width = 145, use_column_width = 145) 

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



# ~~~~~~~~~~~~~~~~~~~~~~~ TO DO ~~~~~~~~~~~~~~~~~~~~~~~ #
#   run model on image
#   display output with bounding boxes and labels
#   display original image
#   display list (with cute emojis?) of how many of each thing you have

# lookup emissions values for each item
# display next to each item
# display total emissions

# cute reference statistics
# lookup what's out of season, add a little out of season list somewhere
# ^^ maybe with alternate veggies to buy
# have a whole other page displaying, by month, which things are in season






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







