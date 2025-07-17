import sys
import json
import cv2
from ultralytics import YOLO
from pathlib import Path

def detect_interactions(people_boxes, vehicle_boxes, threshold=50):
    interactions = []
    for i, person in enumerate(people_boxes):
        for j, vehicle in enumerate(vehicle_boxes):
            x1, y1, x2, y2 = person
            vx1, vy1, vx2, vy2 = vehicle
            # Check if person and vehicle are close (overlapping or nearby)
            if not (x2 < vx1 - threshold or x1 > vx2 + threshold or y2 < vy1 - threshold or y1 > vy2 + threshold):
                interactions.append(f"Person {i+1} near Vehicle {j+1}")
    return interactions

video_path, people_count, vehicle_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
skip_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 1
Path("processed").mkdir(exist_ok=True)

model = YOLO("yolov8s.pt")
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

annotations, alerts = [], []
frame_num = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    if frame_num % skip_frames == 0:
        progress = (frame_num + 1) / total_frames * 100
        print(f"\rProcessing frames: {frame_num + 1}/{total_frames} ({progress:.1f}%)", end="", flush=True)
        
        results = model(frame)
        timestamp = frame_num / fps
        
        people_boxes = [box.xyxy[0].tolist() for box in results[0].boxes if box.cls == 0]  # person class
        vehicle_boxes = [box.xyxy[0].tolist() for box in results[0].boxes if box.cls in [2, 3, 5, 7]]  # car, motorcycle, bus, truck
        
        annotations.append({
            "frame": frame_num,
            "timestamp": timestamp,
            "people": len(people_boxes),
            "vehicles": len(vehicle_boxes),
            "people_boxes": people_boxes,
            "vehicle_boxes": vehicle_boxes
        })
        
        if len(people_boxes) > people_count:
            alerts.append({"timestamp": timestamp, "alert": f"Suspicious Activity: There are {len(people_boxes)} suspects in the footage!"})
        
        if len(vehicle_boxes) > vehicle_count:
            alerts.append({"timestamp": timestamp, "alert": f"Suspicious Activity: There are {len(vehicle_boxes)} suspicious vehicles in the footage!"})
        
        interactions = detect_interactions(people_boxes, vehicle_boxes)
        for interaction in interactions:
            alerts.append({"timestamp": timestamp, "alert": f"Security Alert: {interaction}"})
    
    frame_num += 1

print()  # New line when done
cap.release()

base_name = Path(video_path).stem
with open(f"processed/{base_name}_annotations.json", "w") as f:
    json.dump(annotations, f, indent=2)
with open(f"processed/{base_name}_alerts.json", "w") as f:
    json.dump(alerts, f, indent=2)

"""
Examples:
uv run python 02_process_video.py "downloads/1gi5qn1khVk_15.webm" 1 0 5
uv run python 02_process_video.py "downloads/IDN4S-mhplk_21.webm" 0 0 5
uv run python 02_process_video.py "downloads/KTDen9ooazo_22.webm" 2 0 5
uv run python 02_process_video.py "downloads/ms-Q3t5IqNM_12.webm" 0 1 5
uv run python 02_process_video.py "downloads/p_sOLAtXY44_28.webm" 0 1 5
uv run python 02_process_video.py "downloads/V3QMrftx3cQ_32.webm" 0 0 5
"""