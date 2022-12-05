import torch
import utils
display = utils.notebook_init()  # checks

def get_fruit_text(img_path):
    !python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source img_path