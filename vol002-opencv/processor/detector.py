import cv2


class PersonDetector:
    def __init__(self, classifier_path):
        self._cascade_classifier = cv2.CascadeClassifier(classifier_path)

    def identifier(self, image):
        return self._cascade_classifier.detectMultiScale(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            scaleFactor=1.11,
            minNeighbors=3,
            minSize=(50, 50))

    def marking(self, image, rectangles, frame_color=(0, 0, 255)):
        for (x, y, w, h) in rectangles:
            cv2.rectangle(image, (x, y), (x + w, y + h), frame_color, thickness=2)
