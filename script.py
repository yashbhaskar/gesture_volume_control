import cv2
import numpy as np
import handtrackingmodule as ht
import math
import time
#############################
###############################
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minValue = volRange[0]
maxValue = volRange[1]
#volume.SetMasterVolumeLevel(0.0, None)
#####################################
###################################
cap = cv2.VideoCapture(0)
hand_tracking = ht.Hands()
ptime = 0
volBar = 400
volPer = 0
while True:
    ret, frame = cap.read()
    if ret:
        frame = hand_tracking.findHands(frame,draw=True)
        lmList = hand_tracking.findPosition(frame, draw=False)
        if len(lmList) != 0:
            x1, y1= lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.circle(frame, (lmList[4][1], lmList[4][2]), 10, (255,0,255), cv2.FILLED)
            cv2.circle(frame, (lmList[8][1], lmList[8][2]), 10, (255,0,255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255,100, 255), 3)
            cx, cy = (x1+x2)//2, (y1+y2)//2
            cv2.circle(frame, (cx, cy), 10, (255, 100, 255), cv2.FILLED)
            length = math.hypot(x2-x1, y2-y2)
            #print("Length", length)
            vol = np.interp(length, [18, 260], [minValue, maxValue])
            volBar = np.interp(length, [18, 260], [400, 150])
            volPer = np.interp(length, [18, 260], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime=ctime
        cv2.putText(frame, f'FPS: {int(fps)}', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255,100,100), 2)
        cv2.rectangle(frame, (50,150), (85, 400), (255, 0,0), 3)
        cv2.rectangle(frame, (50,int(volBar)), (85, 400), (255, 100,100), cv2.FILLED)
        cv2.putText(frame, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 100, 100), 4)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('1'):
            break
    else:
        break
