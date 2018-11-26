import cv2

# cascade へのパスは絶対パスで指定
face_classifier = '/home/pi/IoT-Hands-on/vol002-surveillance-camera/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_classifier)
# color = [B, G, R]
COLOR = [0, 0, 255]


def person_identifier(photo_name):
    img = cv2.imread(photo_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=3, minSize=(50, 50))

    if len(faces) >= 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), COLOR, thickness=2)

        photo_name = 'detected_' + photo_name
        cv2.imwrite(photo_name, img)

    return len(faces), photo_name
