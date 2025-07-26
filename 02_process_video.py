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
                interactions.append(f"Persona {i+1} cerca del Vehículo {j+1}!!!")
    
    for i, person_1 in enumerate(people_boxes):
        for j, person_2 in enumerate(people_boxes):
            if i!=j:
                x1, y1, x2, y2 = person_1
                vx1, vy1, vx2, vy2 = person_2
                # Check if person_1 and person_2 are close (overlapping or nearby)
                if not (x2 < vx1 - threshold or x1 > vx2 + threshold or y2 < vy1 - threshold or y1 > vy2 + threshold):
                    interactions.append(f"Persona {i+1} cerca de la Persona {j+1}!!!")
    return interactions

video_id, people_count, vehicle_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
skip_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 1
Path("annotations").mkdir(exist_ok=True)
Path("processed").mkdir(exist_ok=True)

model = YOLO("yolov8s.pt")
cap = cv2.VideoCapture(f"downloads/{video_id}.webm")
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
        
        people_boxes = [box.xyxy[0].tolist() for box in results[0].boxes if box.cls == 0]  # Clase Persona
        vehicle_boxes = [box.xyxy[0].tolist() for box in results[0].boxes if box.cls in [2, 3, 5, 7]]  # Auto, Moto, Bus, Camión
        
        annotations.append({
            "frame": frame_num,
            "timestamp": timestamp,
            "people": len(people_boxes),
            "vehicles": len(vehicle_boxes),
            "people_boxes": people_boxes,
            "vehicle_boxes": vehicle_boxes
        })

        if len(people_boxes) == people_count:
            alerts.append({"timestamp": timestamp, "alert": "Todo OK"})
        
        if len(people_boxes) > people_count:
            alerts.append({"timestamp": timestamp, "alert": "Actividad Sospechosa"})

        
        if len(vehicle_boxes) > vehicle_count:
            alerts.append({"timestamp": timestamp, "alert": "Actividad Sospechosa"})
        
        interactions = detect_interactions(people_boxes, vehicle_boxes)
        for interaction in interactions:
            alerts.append({"timestamp": timestamp, "alert": "¡Alerta de Seguridad!"})
    
    frame_num += 1


cap.release()

with open(f"annotations/{video_id}_annotations.json", "w") as f:
    json.dump(annotations, f, indent=2)
with open(f"processed/{video_id}_alerts.json", "w") as f:
    json.dump(alerts, f, indent=2)

"""
Examples:
uv run python 02_process_video.py "KTDen9ooazo" 2 0
uv run python 02_process_video.py "1gi5qn1khVk" 1 0
uv run python 02_process_video.py "IDN4S-mhplk" 0 0
uv run python 02_process_video.py "ms-Q3t5IqNM" 0 1
uv run python 02_process_video.py "p_sOLAtXY44" 0 1
uv run python 02_process_video.py "V3QMrftx3cQ" 0 0
"""