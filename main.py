from ultralytics import YOLO
import cv2
import time

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

log_file = open("logs/events_log.txt", "a")

prev_state = ""
log_lines = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame_area = h * w

    results = model.track(frame, persist=True)

    annotated_frame = frame.copy()
    system_state = "NORMAL"
    active_ids = []

    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls = int(box.cls[0])

            if cls == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                track_id = int(box.id[0]) if box.id is not None else -1

                active_ids.append(track_id)

                box_area = (x2 - x1) * (y2 - y1)
                ratio = box_area / frame_area

                if ratio < 0.04:
                    color = (0,255,0)
                    label = "SAFE"
                elif ratio < 0.08:
                    color = (0,255,255)
                    label = "WARNING"
                else:
                    color = (0,0,255)
                    label = "DANGER"

                if label == "DANGER":
                    system_state = "STOP"
                elif label == "WARNING" and system_state != "STOP":
                    system_state = "SLOW"

                cv2.rectangle(annotated_frame, (x1,y1), (x2,y2), color, 2)
                cv2.putText(annotated_frame, f"ID:{track_id} {label}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # =========================
    # Robot Simulation
    # =========================
    if system_state == "STOP":
        speed = 0
    elif system_state == "SLOW":
        speed = 50
    else:
        speed = 100

    # Logging
    if system_state != prev_state:
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"{timestamp} | {system_state} | IDs:{active_ids} | Speed:{speed}"
        log_lines.append(log_entry)
        log_file.write(log_entry + "\n")
        prev_state = system_state

    # =========================
    # Draw system info
    # =========================
    if system_state == "STOP":
        state_color = (0,0,255)
    elif system_state == "SLOW":
        state_color = (0,255,255)
    else:
        state_color = (0,255,0)

    cv2.putText(annotated_frame, f"SYSTEM: {system_state}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, state_color, 3)

    cv2.putText(annotated_frame, f"SPEED: {speed}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # =========================
    # Dashboard panel
    # =========================
    panel = annotated_frame[:, :300] * 0  # black panel

    y = 30
    for line in log_lines[-10:]:
        cv2.putText(panel, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        y += 25

    dashboard = cv2.hconcat([annotated_frame, panel])

    cv2.imshow("Safety Dashboard", dashboard)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
log_file.close()
cv2.destroyAllWindows()