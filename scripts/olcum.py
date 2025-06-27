import cv2
from ultralytics import YOLO
import numpy as np
import time

# kullanılan silginin genişliği cm cinsinden cetvel ile hesaplanmıştır.
KNOWN_WIDTH_ERASER = 4.0 

# cam_calibrate.py Kalibrasyonla bulunan, kamerama özel odak uzaklığı değeri
FOCAL_LENGTH = 705

model = YOLO("../distance_model/weights/best.pt")

# data.yaml dosyasından sınıf isimi alınıyor.
class_names = model.names

# Webcam'i açma
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Hata: Webcam açılamadı.")
    exit()

while True:
    success, frame = cap.read()
    if not success:
        break

    # Modeli bu kare üzerinde çalıştır ve nesneleri tespit et
    results = model(frame)

    # Tespit edilen her nesne için döngü
    for r in results:
        time.sleep(4)
        boxes = r.boxes
        for box in boxes:
            # Sınıf ID'sini ve ismini al
            cls_id = int(box.cls[0])
            class_name = class_names[cls_id]

            if class_name == 'eraser':
                # Tespitin güven skorunu al
                conf = float(box.conf[0])
                
                # Sadece %50'den daha güvenli tespitleri göster
                if conf > 0.5:
                    # Dikdörtgenin koordinatlarını al (x1, y1, x2, y2)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Dikdörtgenin piksel cinsinden genişliğini hesapla
                    pixel_width = x2 - x1

                    # Uzaklık formülünü uygula
                    if pixel_width > 0:
                        # known_width olarak doğrudan silginin genişliğini kullanıyoruz
                        distance = (KNOWN_WIDTH_ERASER * FOCAL_LENGTH) / pixel_width

                        label = f'Silgi: {distance:.2f} cm'

                        # Dikdörtgeni çiz
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

                        # Yazıyı sol üst köşeye yaz
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)


    cv2.imshow("Webcam - Sadece Silgi Mesafe Tespiti (Cikis icin 'q')", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()