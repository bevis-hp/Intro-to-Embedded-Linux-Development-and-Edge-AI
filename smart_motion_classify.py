import cv2
import sys
import time
from ultralytics import YOLO

# Define the camera ID
camera_id = 0

def run_smart_pipeline(cam_id):
    # Initialize the video stream
    video_capture = cv2.VideoCapture(cam_id)

    if not video_capture.isOpened():
        print(f"Error: Could not open camera {cam_id}.")
        sys.exit(1)

    print("Loading specialized YOLO classification model...")
    # Load the classification-only model (much faster, no localization)
    classifier_model = YOLO("yolov26n-cls.pt")

    print("Smart Pipeline started!")
    print("IMPORTANT: Ensure the camera is pointed at a static background.")
    print("Warming up camera sensor for 2 seconds...")
    
    # Let the camera auto-exposure and auto-white-balance settle
    time.sleep(2)
    
    # Grab the baseline frame for motion detection
    read_success, first_frame = video_capture.read()
    if not read_success:
        sys.exit(1)

    gray_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    blurred_first_frame = cv2.GaussianBlur(gray_first_frame, (21, 21), 0)

    while True:
        read_success, current_frame = video_capture.read()
        if not read_success:
            break

        # --- MOTION DETECTION MATH ---
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        blurred_current = cv2.GaussianBlur(gray_current, (21, 21), 0)
        frame_delta = cv2.absdiff(blurred_first_frame, blurred_current)
        _, thresh_frame = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        motion_contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get the total area of the video frame to filter out lighting glitches
        frame_height, frame_width = current_frame.shape[:2]
        max_contour_area = (frame_width * frame_height) * 0.75 

        # --- CLASSIFYING ONLY THE MOVING OBJECTS ---
        for contour in motion_contours:
            contour_area = cv2.contourArea(contour)
            
            # Ignore tiny movements and massive lighting changes
            if contour_area < 2000 or contour_area > max_contour_area:
                continue

            # Get the coordinates of the moving object
            (box_x, box_y, box_w, box_h) = cv2.boundingRect(contour)

            # Crop the original color frame down to just the moving object's bounding box
            # Python arrays slice as [y_start:y_end, x_start:x_end]
            frame_crop = current_frame[box_y:box_y+box_h, box_x:box_x+box_w]

            # Failsafe: ensure the crop isn't empty before passing to AI
            if frame_crop.size != 0:
                # Pass ONLY the tiny cropped image to the classifier
                ai_results = classifier_model(frame_crop, verbose=False)
                
                # Extract the top predicted class name
                top_prediction = ai_results[0].names[ai_results[0].probs.top1]

                # Draw the green bounding box
                cv2.rectangle(current_frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 255, 0), 2)
                
                # Write the AI's prediction above the box
                cv2.putText(current_frame, top_prediction, (box_x, box_y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the final optimized feed
        cv2.imshow("Smart Edge AI Pipeline", current_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_smart_pipeline(camera_id)
