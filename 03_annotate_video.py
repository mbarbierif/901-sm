import sys
import json
import cv2
from pathlib import Path

string_id = sys.argv[1]

# Load annotations
with open(f"processed/{string_id}_annotations.json", "r") as f:
    annotations = json.load(f)

# Open input video
cap = cv2.VideoCapture(f"downloads/{string_id}.webm")
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Setup output video
fourcc = cv2.VideoWriter_fourcc(*'VP80')
out = cv2.VideoWriter(f"processed/{string_id}_annotated.webm", fourcc, fps, (width, height))

# Create frame lookup for annotations
frame_annotations = {ann["frame"]: ann for ann in annotations}

frame_num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    progress = (frame_num + 1) / total_frames * 100
    print(f"\rAnnotating frames: {frame_num + 1}/{total_frames} ({progress:.1f}%)", end="", flush=True)
    
    # Draw annotations if available for this frame
    if frame_num in frame_annotations:
        ann = frame_annotations[frame_num]
        
        # Draw people boxes in green
        for box in ann["people_boxes"]:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw vehicle boxes in blue
        for box in ann["vehicle_boxes"]:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "Vehicle", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Add count overlay
        cv2.putText(frame, f"People: {ann['people']} | Vehicles: {ann['vehicles']}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    out.write(frame)
    frame_num += 1

print()  # New line when done
cap.release()
out.release()

"""
Examples:
uv run python 03_annotate_video.py "1gi5qn1khVk_15"
uv run python 03_annotate_video.py "IDN4S-mhplk_21"
uv run python 03_annotate_video.py "KTDen9ooazo_22"
uv run python 03_annotate_video.py "ms-Q3t5IqNM_12"
uv run python 03_annotate_video.py "p_sOLAtXY44_28"
uv run python 03_annotate_video.py "V3QMrftx3cQ_32"
"""