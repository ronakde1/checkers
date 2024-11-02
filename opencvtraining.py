import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# Step 1: Load images and labels
def load_images_and_labels(data_directory):
    images = []
    labels = []
    label_map = {'red_checker': 0, 'blue_checker': 1, 'no_checker_white': 2,'no_checker_black': 3}

    for label_name, label in label_map.items():
        folder_path = os.path.join(data_directory, label_name)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            image = cv2.imread(img_path)
            if image is not None:
                images.append(cv2.resize(image, (64, 64)))  # Resize to 64x64
                labels.append(label)

    return np.array(images), np.array(labels)

# Step 2: Preprocess and split the data
data_directory = 'training'
images, labels = load_images_and_labels(data_directory)
images = images.astype('float32') / 255.0  # Normalize pixel values
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Step 3: Feature extraction (using flattening for SVM)
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Step 4: Train the SVM classifier
classifier = SVC(kernel='linear')
classifier.fit(X_train_flat, y_train)

# Step 5: Evaluate the model
y_pred = classifier.predict(X_test_flat)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Step 6: Make predictions on new images
def predict_image(image_path):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (64, 64)).astype('float32') / 255.0
    image_flat = image_resized.flatten().reshape(1, -1)
    prediction = classifier.predict(image_flat)
    return prediction

# Example usage
predicted_label = predict_image('blue.png')
hello=predicted_label[0]
print(["red checker","blue checker","no checker white", "no checker black"][hello])

