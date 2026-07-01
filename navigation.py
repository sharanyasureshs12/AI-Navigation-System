from ultralytics import YOLO
import cv2
import win32com.client
import winsound
import time

# ==============================
# Load YOLO Model
# ==============================

model = YOLO("yolov8n.pt")

# ==============================
# Voice Assistant
# ==============================

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# ==============================
# Camera
# ==============================

cap = cv2.VideoCapture(0)

# ==============================
# Variables
# ==============================

last_time = 0
last_message = ""

important = [
    "person",
    "chair",
    "bottle",
    "car",
    "bus",
    "bicycle",
    "motorcycle",
    "table"
]

# ==============================
# FPS
# ==============================

prev_frame_time = 0

# ==============================
# Main Loop
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_width = frame.shape[1]

    results = model(frame)

    detections = []

    # ==========================
    # Detect Objects
    # ==========================

    for r in results:

        for box in r.boxes:

            cls = int(box.cls[0])

            label = model.names[cls]

            confidence = float(box.conf[0])

            if label not in important:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            x_center = (x1 + x2) // 2

            # Direction

            if x_center < frame_width / 3:

                direction = "Left"

            elif x_center > 2 * frame_width / 3:

                direction = "Right"

            else:

                direction = "Ahead"

            # Distance

            area = (x2 - x1) * (y2 - y1)

            if area > 70000:

                distance = "Very Close"

            elif area > 40000:

                distance = "Close"

            elif area > 15000:

                distance = "Medium"

            else:

                distance = "Far"

            detections.append({

                "label": label,
                "confidence": confidence,
                "direction": direction,
                "distance": distance,
                "box": (x1, y1, x2, y2)

            })

    # ==========================
    # Voice Every 2 Seconds
    # ==========================

    current_time = time.time()

    if current_time - last_time > 2:

        if detections:

            first = detections[0]

            message = (
                f"Warning! "
                f"{first['label']} detected "
                f"{first['direction']}. "
                f"{first['distance']}."
            )

        else:

            message = "Path Clear"

        if message != last_message:

            print(message)

            winsound.Beep(1000, 200)

            speaker.Speak(message)

            last_message = message

        last_time = current_time

    # ==========================
    # Draw Bounding Boxes
    # ==========================

    for item in detections:

        x1, y1, x2, y2 = item["box"]

        cv2.rectangle(

            frame,

            (x1, y1),

            (x2, y2),

            (0, 255, 0),

            2

        )

        text = (
            f"{item['label']} "
            f"{item['confidence']*100:.1f}%"
        )

        cv2.putText(

            frame,

            text,

            (x1, y1 - 10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (0, 255, 255),

            2

        )

        cv2.putText(

            frame,

            item["direction"],

            (x1, y2 + 20),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            item["distance"],

            (x1, y2 + 45),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 0, 255),

            2

        )

    # ==========================
    # Save Detection History
    # ==========================

    if detections:

        with open("detections.txt", "a") as file:

            for item in detections:

                file.write(

                    f"{time.strftime('%H:%M:%S')} | "

                    f"{item['label']} | "

                    f"{item['direction']} | "

                    f"{item['distance']} | "

                    f"{item['confidence']*100:.1f}%\n"

                )

    # ==========================
    # FPS Counter
    # ==========================

    new_frame_time = time.time()

    fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time else 0

    prev_frame_time = new_frame_time

    cv2.putText(

        frame,

        f"FPS : {int(fps)}",

        (20, 30),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (255, 255, 0),

        2

    )

    # ==========================
    # Show Frame
    # ==========================

    cv2.imshow("AI Navigation System", frame)

    # ESC to Exit

    if cv2.waitKey(1) & 0xFF == 27:

        break

# ==============================
# Cleanup
# ==============================

cap.release()

cv2.destroyAllWindows()