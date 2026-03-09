import cv2
import sys
import time

# Define the camera ID
camera_id = 0

def detect_motion(cam_id):
    # Initialize the video capture stream
    video_capture = cv2.VideoCapture(cam_id)

    if not video_capture.isOpened():
        print(f"Error: Could not open camera {cam_id}.")
        sys.exit(1)

    print("Motion detection started!")
    print("IMPORTANT: Ensure the camera is pointed at a static background when starting.")
    print("Warming up camera sensor for 2 seconds...")
    
    # Let the camera auto-exposure and auto-white-balance settle
    time.sleep(2)

    # Grab the very first frame to use as our static background baseline
    read_success, first_frame = video_capture.read()
    
    if not read_success:
        print("Error: Could not read the first frame.")
        sys.exit(1)

    # Convert the baseline frame to grayscale and blur it
    # Blurring removes high-frequency noise/static that might look like tiny movements
    gray_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    blurred_first_frame = cv2.GaussianBlur(gray_first_frame, (21, 21), 0)

    while True:
        # Read the current frame from the camera
        read_success, current_frame = video_capture.read()

        if not read_success:
            print("Error: Frame dropped.")
            break

        # Process the current frame the exact same way as the baseline
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        blurred_current = cv2.GaussianBlur(gray_current, (21, 21), 0)

        # Compute the absolute difference between the current frame and the baseline
        frame_delta = cv2.absdiff(blurred_first_frame, blurred_current)

        # Apply a threshold
        _, thresh_frame = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)

        # Dilate the thresholded image to fill in gaps
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Find the contours (outlines) of the white shapes
        motion_contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get the total area of the video frame to filter out lighting glitches
        frame_height, frame_width = current_frame.shape[:2]
        max_contour_area = (frame_width * frame_height) * 0.75 

        # Loop through all the distinct moving objects we found
        for contour in motion_contours:
            contour_area = cv2.contourArea(contour)
            
            # If the moving object is too small OR too large (lighting glitch), ignore it
            if contour_area < 500 or contour_area > max_contour_area:
                continue

            # Calculate the bounding box for the moving object
            (box_x, box_y, box_w, box_h) = cv2.boundingRect(contour)
            
            # Draw a green rectangle around it on the color frame
            cv2.rectangle(current_frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 255, 0), 2)

        # Display the feeds
        cv2.imshow("Motion Detection", current_frame)
        cv2.imshow("Threshold (The Math)", thresh_frame)

        # Check for the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up hardware and GUI resources
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion(camera_id)
