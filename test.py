import cv2

# Initialize camera (try 0, 1, or -1 if default doesn't work)
cap = cv2.VideoCapture(-1)  # 0 = default camera

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera!")
    exit()

print("Camera opened successfully. Press 'q' to quit.")

while True:
    # Read a frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame (ret=False)")
        break
    
    # Display the frame
    cv2.imshow('Camera Test', frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Camera released.")
