import torch
import utils
display = utils.notebook_init()  # checks

img_path = './test/apple.jpeg'

detected = !python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source img_path

print(detected)

# def get_fruit_text(img_path):
#   detected = !python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source img_path
#   return detected

# get_fruit_text()

