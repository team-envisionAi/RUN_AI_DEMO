# -*- coding: utf-8 -*-
"""Salad.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1buShGXHFUasZixZLpbcXEjNqdqW6gQN2
"""

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

Crowding_path = "short_video_3.mp4"

import supervision as sv
print("supervision", sv.__version__)

sv.VideoInfo.from_video_path(Crowding_path)

from ultralytics import YOLO

# Load the YOLOv9 model
model = YOLO('yolov9e.pt')

# Commented out IPython magic to ensure Python compatibility.
from supervision import Detections
import numpy as np
import supervision as sv
import cv2



# Define the codec using VideoWriter_fourcc and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi', fourcc, 25.0, (1280, 700))



# initiate polygon zone
polygon = np.array([
     [133, 303],[673, 113],[1167, 336],[1020, 690],[230, 690],[133, 306]
])
video_info = sv.VideoInfo.from_video_path(Crowding_path)
zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white(), thickness=2, text_thickness=2, text_scale=0.8)

# extract video frames
generator = sv.get_video_frames_generator(Crowding_path)
iterator = iter(generator)

for frame in iterator:
    frame = cv2.resize(frame, (1280, 700))
    results = model.predict(frame)

    # detect
    results = model(frame, conf=0.1, imgsz=1280)[0]
    detections = sv.Detections.from_ultralytics(results)

    # Filter detections to include only humans
    human_indices = np.where(detections.class_id == 0)[0]
    xyxy = detections.xyxy[human_indices]
    confidence = detections.confidence[human_indices]
    class_id = detections.class_id[human_indices]

    # Create Detections object
    detections = sv.Detections(xyxy=xyxy, confidence=confidence, class_id=class_id, tracker_id=None)
    mask = zone.trigger(detections=detections)

    # annotate
    box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=0.2)
    labels = [f"{model.names[class_id]} {confidence:0.2f}" for xyxy, confidence, class_id in zip(detections.xyxy, detections.confidence, detections.class_id)]
    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
    frame = zone_annotator.annotate(scene=frame)

    # Add count of people in the zone to the frame
    count = np.sum(mask)
    print(count)
    print("-----------------------------------------")
    cv2.putText(frame, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    out.write(frame)

# After writing all frames, release the video writer
out.release()
