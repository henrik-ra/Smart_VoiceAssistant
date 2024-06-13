import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os


background_images_path = 'Smart_VoiceAssistant/pics'

if not os.path.exists(background_images_path):
    raise FileNotFoundError(f'Das Verzeichnis {background_images_path} existiert nicht')

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise Exception("Kamera konnte nicht geöffnet werden")

segmentor = SelfiSegmentation()

# Hintergrundbilder einlesen und auf 640x480 skalieren
listImg = os.listdir(background_images_path)
imgList = []
for imgPath in listImg:
    img = cv2.imread(os.path.join(background_images_path, imgPath))
    img = cv2.resize(img, (640, 480))
    imgList.append(img)

indexImg = 0

while True:
    success, img = camera.read()
    if not success or img is None:
        print("Bild konnte nicht von der Kamera gelesen werden")
        break
    
    # Webcam-Bild auf 640x480 skalieren
    try:
        img = cv2.resize(img, (640, 480))
    except cv2.error as e:
        print("Fehler beim Skalieren des Bildes: ", e)
        break

    # Hintergrund entfernen und mit Hintergrundbild kombinieren
    imgOut = segmentor.removeBG(img, imgList[indexImg])
    
    # Video anzeigen
    cv2.imshow("Image", imgOut)
    key = cv2.waitKey(1)
    
    # Navigation und Beenden
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1
    elif key == ord('d'):
        if indexImg < len(imgList) - 1:
            indexImg += 1
    elif key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
