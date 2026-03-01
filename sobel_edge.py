import cv2
import numpy as np
import sys

# Define the target image
target_image = "test_image.jpg"

def process_image(file_path):
    # Load the image
    source_image = cv2.imread(file_path)
    
    if source_image is None:
        print(f"Error: Could not load {file_path}. Did you download it?")
        sys.exit(1)

    # Convert the image to grayscale (edges don't need color)
    gray_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

    # Apply Sobel filter to find horizontal and vertical edges
    # The cv2.CV_64F allows for negative values during calculation
    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    # Convert back to absolute values and 8-bit image format
    abs_sobel_x = cv2.convertScaleAbs(sobel_x)
    abs_sobel_y = cv2.convertScaleAbs(sobel_y)

    # Combine the horizontal and vertical edges into one image
    combined_edges = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

    # Display the original and the edge-detected result
    cv2.imshow("Original Image", source_image)
    cv2.imshow("Sobel Edge Detection", combined_edges)

    print("Press any key in the image window to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image(target_image)
