import cv2
import time
import os
import ElizlemeModulu as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

if not cap.isOpened():
    print("Kamera açılamıyor. Lütfen kamerayı kontrol edin.")
    exit()

folderPath = "ParmakResimleri"
myList = os.listdir(folderPath)
myList = sorted([f for f in myList if not f.startswith('.')])  # Gizli dosyaları atla ve sıralama
overlayList = []

# Görselleri yükleyin
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    if image is not None:
        overlayList.append(image)
    else:
        print(f"{imPath} yüklenemedi.")
print(f"Yüklenen görsel sayısı: {len(overlayList)}")

pTime = 0
detector = htm.handDetector(detectionCon=0.75, trackCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    
    if not success or img is None:
        print("Kamera görüntüsü alınamadı.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        fingers = []
        # Başparmak
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Parmak
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        print("Hesaplanan Parmak Sayısı:", totalFingers)
        
        # Görsel seçimi için doğru bir aralık kontrolü
        if 1 <= totalFingers <= len(overlayList):
            print(f"Görsel İndeksi: {totalFingers - 1}")
            h, w, c = overlayList[totalFingers - 1].shape
            img[0:h, 0:w] = overlayList[totalFingers - 1]
            cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        else:
            print("Geçersiz parmak sayısı:", totalFingers)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    
    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



