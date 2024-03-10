import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input("Enter a numeric user ID here: ")

print("Taking Samples, Look at the camera...")

count = 0

while True:
    ret, image = cam.read()
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(img, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1

        cv2.imwrite("samples/face." + str(count) + ".jpg", img[y: y+h, x: x+w])
        cv2.imshow('image', image)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 10:
        break

print("Sample Taken Now, Closing the program...")
cam.release()
cv2.destroyAllWindows()
