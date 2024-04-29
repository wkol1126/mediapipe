import cv2 as cv
import mediapipe as mp
import time, math


class handDetector:
    def __init__(self, mode=False, num_hands=2, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.num_hands = num_hands
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        

    def find_hands(self, img, show_links=True):        
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks and show_links:
            for handLms in results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

    def find_finger(self, img, fingerID=0):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results =self.hands.process(imgRGB)
        self.finger_pos = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):                     
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cz = lm.z
                    self.finger_pos.append([cx, cy, cz])
            return self.finger_pos[fingerID][0], self.finger_pos[fingerID][1], True
        else:
            return 0, 0, False

    def finger_distance(self, ind1, ind2):
        pos1 = self.finger_pos[ind1]
        pos2 = self.finger_pos[ind2]
        return int(math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2))

    def figer_depth(self, ind):
        return self.finger_pos[ind][2]

def main():
    cap = cv.VideoCapture(0)
    previus_time =0 
    current_time = 0
    detector = handDetector()
    while True:
        sucess, frame = cap.read()
        frame = cv.flip(frame, 1)
        detector.find_hands(frame)
    
        current_time = time.time()
        fps = 1/(current_time - previus_time)
        previus_time = current_time
        cv.putText(frame, 'fps=' + str(int(fps)), (10,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)

        cv.imshow('Camera', frame)   
    
        if cv.waitKey(5) & 0xFF == ord('d'):
            cap.release()    
            break
if __name__ == '__main__':
    main()