import cv2
import numpy as np
from joblib import load  # Import joblib for loading the model

import solver.Square, solver.Piece

# Load the trained SVM classifier
classifier = load('checker_classifier.joblib')

# Define the class names based on your label mapping
class_names = ["red_checker", "blue_checker", "no_checker_white", "no_checker_black"]

# Function to preprocess the image and make a prediction
def predict_image(image_path):
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Please check the path.")
        return None
    
    # Resize and normalize the image
    image_resized = cv2.resize(image, (64, 64)).astype('float32') / 255.0
    image_flat = image_resized.flatten().reshape(1, -1)  # Flatten the image

    # Make the prediction
    prediction = classifier.predict(image_flat)
    
    return prediction[0]  # Return the predicted class index

# Main function to run the program
def main():
    # Input image path from the user
    image_path = "red.png"
    
    # Get the predicted class
    predicted_label_index = predict_image(image_path)
    
    if predicted_label_index is not None:
        # Print the corresponding class name
        print(f"The predicted label is: {class_names[predicted_label_index]}")
    
        if class_names[predicted_label_index] == "red_checker":
            return Square(Piece(_is_ai=True, _is_king=False))

# Run the main function
if __name__ == "__main__":
    main()
