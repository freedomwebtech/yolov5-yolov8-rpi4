import cv2
from yolo_segmentation import YOLOSEG
import cvzone
ys = YOLOSEG("yolov8m-seg.pt")

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

cap=cv2.VideoCapture('p3.mp4')
count=0
while True:
    ret,frame=cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(500,480))
    overlay = frame.copy()
    alpha = 0.7

    bboxes, classes, segmentations, scores = ys.detect(frame)
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
    # print("bbox:", bbox, "class id:", class_id, "seg:", seg, "score:", score)
        (x, y, x2, y2) = bbox
        c=class_list[class_id]
        if 'truck' in c:
            cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)    
            cv2.polylines(frame, [seg], True, (0, 0, 255), 4)
            cv2.fillPoly(overlay, [seg], (0,0,255))
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 2, frame)
            cvzone.putTextRect(frame, f'{c}', (x,y),1,1)

    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
