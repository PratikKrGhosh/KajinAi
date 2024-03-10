import cv2
from cv2 import face
import numpy as np
from PIL import Image
import os

path = "samples"
recognizer = face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def images_and_lebels(p):
    image_paths = [os.path.join(p, f) for f in os.listdir(p)]
    face_samples = []
    all_id = []

    for image_path in image_paths:
        gray_img = Image.open(image_path).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        my_id = int(os.path.split(image_path)[-1].split(".")[1])
        all_faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in all_faces:
            face_samples.append(img_arr[y: y+h, x: x+w])
            all_id.append(my_id)

    return face_samples, all_id


print("Training faces, it will take a few seconds, wait...")

faces, ids = images_and_lebels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('trainer/trainer.yml')
print("Model Trained, Now we can recognize your face")
