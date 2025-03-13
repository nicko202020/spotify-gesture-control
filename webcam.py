import cv2

# Open a connection to the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Display the resulting frame
    cv2.imshow('Webcam Test', frame)

    # Exit the loop when the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()