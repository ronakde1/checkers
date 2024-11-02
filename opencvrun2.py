import cv2
import numpy as np
from joblib import load  # Import joblib for loading the model

from solver import Square, Piece

# Load the trained SVM classifier
classifier = load('checker_classifier.joblib')

# Define the class names based on your label mapping
class_names = ["red_checker", "blue_checker", "no_checker_white", "no_checker_black"]
class_squares = [
    Square(Piece(_is_king=False, _is_ai=True)),
    Square(Piece(_is_king=False, _is_ai=False)),
    Square(),
    Square()
]

# Function to preprocess the image and make a prediction
def predict_image_from_path(image_path):
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Please check the path.")
        return None

    return classify(image)


def classify(image) -> Square:
    # Resize and normalize the image
    image_resized = cv2.resize(image, (64, 64)).astype('float32') / 255.0
    image_flat = image_resized.flatten().reshape(1, -1)  # Flatten the image

    # Make the prediction
    prediction = classifier.predict(image_flat)
    
    return class_squares[prediction[0]]  # Return the predicted square


# Main function to run the program
def main():
    # Input image path from the user
    image_path = "training/blue_checker/blue.png"
    
    # Get the predicted class
    square = predict_image_from_path(image_path)
    
    if square is not None:
        # Print the corresponding class name
        print(f"The predicted square is: {square}")

# Run the main function
if __name__ == "__main__":
    main()
