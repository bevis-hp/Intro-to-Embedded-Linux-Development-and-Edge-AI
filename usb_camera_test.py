import cv2
import sys

# Define the camera ID based on your v4l2-ctl output
# 0 is usually the default for the first plugged-in USB camera
camera_id = 0

def stream_video(cam_id):
    # Initialize the video capture stream using the camera ID
    video_capture = cv2.VideoCapture(cam_id)

    # Check if the camera initialized successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open camera {cam_id}.")
        print("Try changing the camera_id variable to 1 or 2.")
        sys.exit(1)

    print("Camera opened successfully! Press 'q' in the video window to quit.")

    # Create an infinite loop to continuously grab frames from the camera
    while True:
        # read() returns two values: 
        # read_success (a boolean indicating if the frame was grabbed)
        # video_frame (the actual image data array)
        read_success, video_frame = video_capture.read()

        # If a frame drops or the camera disconnects, break the loop
        if not read_success:
            print("Error: Frame dropped or camera disconnected.")
            break

        # Display the live video frame in a GUI window
        cv2.imshow("USB Camera Test Stream", video_frame)

        # Wait for 1 millisecond for a key press
        # If the pressed key is 'q', break out of the infinite loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up: release the hardware camera resource and close all GUI windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video(camera_id)
