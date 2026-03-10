import cv2
import sys
from ultralytics import YOLO

# Define the camera ID
camera_id = 0

def run_yolo(cam_id):
    # Initialize the video capture stream
    video_capture = cv2.VideoCapture(cam_id)

    if not video_capture.isOpened():
        print(f"Error: Could not open camera {cam_id}.")
        sys.exit(1)

    print("Loading YOLO model... (This may download weights on the first run)")
    # Load the YOLO26 nano model
    detection_model = YOLO("yolo26n.pt")
    
    detection_model.export(format="ncnn")

    ncnn_model = YOLO("yolo26n_ncnn_model")

    print("YOLO stream started! Press 'q' in the video window to quit.")

    while True:
        read_success, video_frame = video_capture.read()

        if not read_success:
            print("Error: Frame dropped.")
            break

        # Pass the frame to the YOLO model
        # stream=True keeps it memory efficient for video
        ai_results = ncnn_model(video_frame, stream=True, verbose=False)

        # Iterate through the results and plot them on the frame
        for result in ai_results:
            # result.plot() automatically draws bounding boxes and labels
            annotated_frame = result.plot()

        # Display the live annotated feed
        cv2.imshow("YOLO Live Detection", annotated_frame)

        # Check for the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up hardware and GUI resources
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_yolo(camera_id)
