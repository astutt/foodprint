
# fruit_kg is the avg weight
# fruit_co2 is the co2 emission per kg
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

# dictionary with contents of image. can be any data type, just keep it consistent in the conditionals
detected = {'apples': 2, 'bananas': 2, 'oranges': 2, 'carrots':2, 'broccoli':2}

# conditionals with calcs
if 'apples' in detected:
    apple_em = detected['apples']*apple_kg*apple_co2
    co2_total += apple_em
elif 'bananas' in detected:
    banana_em = detected['bananas']*banana_kg*banana_co2
    co2_total += banana_em
elif 'oranges' in detected:
    orange_em = detected['oranges']*citrus_kg*citrus_co2
    co2_total += orange_em
elif 'carrots' in detected:
    carrot_em = detected['carrots']*carrot_kg*carrot_co2
    co2_total += carrot_em
elif 'broccoli' in detected:
    broccoli_em = detected['broccoli']*broccoli_kg*broccoli_co2
    co2_total += broccoli_em

# total emissions :)
print(co2_total)
print("kg of CO2")