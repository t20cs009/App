import cv2
from fer import FER

# FER detector initialization
detector = FER(mtcnn=True)

# OpenCV setup to capture video from webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam, change if needed
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to grayscale for FER (optional depending on the FER library requirements)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Analyze the frame
    result = detector.detect_emotions(frame)

    # Draw rectangles around the detected faces and label the emotions
    for face in result:
        (x, y, w, h) = face['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        emotion = face['emotions']
        cv2.putText(frame, max(emotion, key=emotion.get), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame with annotations
    cv2.imshow('FER on Webcam', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
