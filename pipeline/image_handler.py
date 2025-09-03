import cv2
from io import BytesIO
import numpy as np
import os

def process_image(image_file):
    in_memory_file = BytesIO()
    image_file.save(in_memory_file)

    image_bytes = in_memory_file.getvalue()
    nparr = np.frombuffer(image_bytes, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Try to load cascade file from multiple locations
    cascade_paths = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'),  # Default OpenCV path

    face_cascade = None
    for cascade_path in cascade_paths:
        if os.path.exists(cascade_path):
            face_cascade = cv2.CascadeClassifier(cascade_path)
            if not face_cascade.empty():
                break
    
    # Check if cascade loaded successfully
    if face_cascade is None or face_cascade.empty():
        print("Error: Could not load cascade file from any location")
        return image_bytes, None
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return image_bytes, None
    
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    (x, y, w, h) = largest_face

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    _, buffer = cv2.imencode(".jpg", img)

    return buffer.tobytes(), largest_face