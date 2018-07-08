# Import OpenCV library
import cv2

# Create Face detection object from OpenCV frontal face Classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier('haarcascade_eye.xml')

class VideoCamera(object):

    def __init__(self):
        # Using OpenCV initiate front facing built-in camera of client machine
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip(image, 1)  # Flip image vertically
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5)

        for x, y, w, h in faces:

            # For each face identified draw rectangle around it
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 3)

            # Extract face alone to detect eyes
            face_gray  = gray_image[y:y+h, x:x+w]

            # Detect eyes
            eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1)

            # Execute only if the number of eyes object identified is less than 3
            if len(eyes) < 3:
                for ex, ey, ew, eh in eyes:
                    if (y+(h/2)) > (y+ey+(eh/2)):  # Eliminate nose being identified as eye

                        # For each eye identified draw rectangle around it
                        cv2.rectangle(image, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255,0,0), 2)

        # JPEGs are being painted on the UI continuously as video stream.
        # However OpenCV identifies the faces on raw images.
        # So before sending response to UI the byte arrays is required to be encode into JPEG.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
