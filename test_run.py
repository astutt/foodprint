import torch
import pandas

# load from torch hub instead of storing locally
# more model settings: https://github.com/ultralytics/yolov5/issues/36

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.25 # NMS confidence threshold
model.max_det = 100 # maximum number of detections per image

# Image
im = 'https://ultralytics.com/images/zidane.jpg'
im = 'test_images/test.png'

# Inference
results = model(im)

results.pandas().xyxy[0]

results.print()