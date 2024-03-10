def face_auth(main, close):
    import cv2
    from cv2 import face

    recognizer = face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minw = 0.1 * cam.get(3)
    minh = 0.1 * cam.get(4)

    while True:
        ret, image = cam.read()
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        all_face = face_cascade.detectMultiScale(
            img,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minw), int(minh))
        )

        for (x, y, w, h) in all_face:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            my_id, accuracy = recognizer.predict(img[y: y+h, x: x+w])

            if accuracy < 100:
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
                cam.release()
                cv2.destroyAllWindows()
                main(close)
