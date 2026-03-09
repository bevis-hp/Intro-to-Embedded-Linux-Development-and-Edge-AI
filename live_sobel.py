import cv2
import sys

# Define the camera ID based on your previous tests
camera_id = 0

def stream_edges(cam_id):
    # Initialize the video capture stream
    video_capture = cv2.VideoCapture(cam_id)

    if not video_capture.isOpened():
        print(f"Error: Could not open camera {cam_id}.")
        sys.exit(1)

    print("Edge detection stream opened successfully! Press 'q' to quit.")

    while True:
        # Read frames continuously
        read_success, video_frame = video_capture.read()

        if not read_success:
            print("Error: Frame dropped.")
            break

        # --- IMAGE PROCESSING IN THE LOOP ---
        
        # 1. Convert the current frame to grayscale
        gray_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)

        # 2. Apply Sobel filter to find horizontal and vertical edges
        sobel_x = cv2.Sobel(gray_frame, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_frame, cv2.CV_64F, 0, 1, ksize=3)

        # 3. Convert back to absolute values and 8-bit image format
        abs_sobel_x = cv2.convertScaleAbs(sobel_x)
        abs_sobel_y = cv2.convertScaleAbs(sobel_y)

        # 4. Combine the horizontal and vertical edges into one image
        combined_edges = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

        # --- END IMAGE PROCESSING ---

        # Display the original live video frame
        cv2.imshow("Original Live Stream", video_frame)
        
        # Display the real-time edge detection frame
        cv2.imshow("Real-Time Sobel Edges", combined_edges)

        # Wait for 1 millisecond and check if 'q' is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up resources
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_edges(camera_id)
