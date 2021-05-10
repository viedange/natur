import cv2
import numpy as np
import mido
import time

outport = mido.open_output('loopMIDI Port 1')

w = 0
#clavierout = [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 3, 15, 27, 39, 51, 63, 75, 87, 99, 111, 123, 6, 18, 30, 42,
             # 54, 66, 78, 90, 102, 114, 126, 8, 20, 32, 44, 56, 68, 80, 92, 104, 116, 10, 22, 34, 46, 58, 70, 82, 94,
              #106, 118]

#clavierout = [0,12,24,36,48,60,72,84,96,108,120,4,16,28,40,52,64,76,88,100,112,124,7,19,31,43,55,67,79,91,103,115]
clavierout = [108,120,4,16,28,40,52,64,76,88,100,112,124,7,19,31,43,55,67,79,91,103,115]

cap = cv2.VideoCapture("resources/dt.mp4")
#cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1920,1080))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)

while cap.isOpened():

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawnContours(frame1, contours, -1, (0, 255, 0), 2)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 1000:
            continue

        # 127 MAX
        if w < 300 and w > 10:
            # if w>30:
            for s in clavierout:
                if w == s:
                    w = w + 1
                    #outport.send(mido.Message('note_off', note=w))
                    outport.send(mido.Message('note_on', note=w))
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame1, "Note: {}".format(w), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 0), 3)

            print(w)
            # if h<200:
            # cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv2.putText(frame1, "Status: {}".format('Movement'), (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            # cv2.putText(frame1, "{}".format(w), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 0), 3)
            # cv2.putText(frame1, "human", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (200, 200, 0), 2)

    # cv2.drawContours(frame1, contours, -1      , (0, 255, 0), 2)

    # image = cv2.resize(frame1, (1920,1080))
    # out.write(image)
    #cv2.namedWindow("feed", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("feed", 1920,1440)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
