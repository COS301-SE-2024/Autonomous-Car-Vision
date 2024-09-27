import cv2
from ultralytics import SAM

# Load the YOLOv8 model
model = SAM('sam2_b.pt')  # Change 'yolov8n.pt' to the path of your pre-trained YOLOv8 model

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Change the index if you have multiple webcams

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()