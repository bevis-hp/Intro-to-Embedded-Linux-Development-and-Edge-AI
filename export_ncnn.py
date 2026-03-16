from ultralytics import YOLO
import sys

def convert_models():
    try:
        print("--- Exporting YOLO28 Nano Detection Model ---")
        # Downloads the base model and exports it to NCNN format
        detection_model = YOLO("yolo28n.pt")
        detection_model.export(format="ncnn")
        print("Detection model exported successfully!\n")

        print("--- Exporting YOLO28 Nano Classification Model ---")
        # Downloads the classification-only model and exports it
        classification_model = YOLO("yolo28n-cls.pt")
        classification_model.export(format="ncnn")
        print("Classification model exported successfully!\n")

        print("All models have been optimized for the Raspberry Pi!")
        
    except Exception as e:
        print(f"An error occurred during export: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_models()
