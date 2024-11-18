import cv2
import serial
import time

# Set up serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the connection to establish

# Initialize OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)  # Use your webcam (index might need to be adjusted)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        print("Face detected!")
        arduino.write(b'0')  
    else:
        print("No face detected.")
        arduino.write(b'1') 

    # Display the video feed
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
