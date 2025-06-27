import cv2
from ultralytics import YOLO

model = YOLO("../distance_model/weights/best.pt")
# Sınıf isimlerini al
class_names = model.names

# Webcam'i başlat
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Modeli çalıştır
    results = model(frame)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = float(box.conf[0])
            if conf > 0.6: 
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Piksel genişliğini hesapla
                pixel_width = x2 - x1
                
                cls_id = int(box.cls[0])
                class_name = class_names[cls_id]

                # Terminale yazdır
                print(f"Nesne: {class_name}, Piksel Genişliği (P): {pixel_width}")

                # Ekrana yazdır
                label = f"Piksel Genisligi: {pixel_width}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Kalibrasyon - (Cikis icin 'q')", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()