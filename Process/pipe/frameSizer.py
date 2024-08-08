import cv2

def get_video_frame_sizes(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_index = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            # Break the loop if no more frames are available
            break

        # Get frame dimensions
        height, width, channels = frame.shape

        print(f"Frame {frame_index}: Width = {width}, Height = {height}")

        frame_index += 1

    # Release the video capture object
    cap.release()
    print("Finished processing video.")

# Replace 'video.mp4' with the path to your video file
video_path = 'petal.mp4'
get_video_frame_sizes(video_path)
