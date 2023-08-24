import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3,1280)   #width
cap.set(4,720)    #height

detector = HandDetector(detectionCon=0.8)   #by default its 0.5 but we don't want to press any keys so we give it littlwe bit higher

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"]
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
       ]

finalText = ""

keyboard = Controller()

# # For Normal background
def drawAll(img,buttonList):

    for button in buttonList:
        x,y = button.pos
        w,h = button.size 
        cv2.rectangle(img, button.pos, (x+w,y+h), (255,0,255), cv2.FILLED)
        # hm upper wali line ki jgh ye bhi likh skte h
        # cvzone.cornerRect(img, (button.pos[0], button.pos[1],button.size[0],button.size[0]), 20 ,rt=0)
        cv2.putText(img, button.text, (x+20, y+65) , cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    return img  

# For trans-parent background
# def drawAll(img,buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#             x,y = button.pos
#             cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],button.size[0],button.size[0]), 20 ,rt=0)
#             cv2.rectangle(imgNew, button.pos, (x+button.size[0], y+button.size[1]),
#                           (255,0,255),cv2.FILLED)
#             cv2.putText(imgNew, button.text, (x+40, y+60), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
    
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha,0)[mask]
#     return out



#beacause we have more than one button, so we use class to store them
class Button():
    # this function run only one time begin the loop , so we make another function draw that will change in every loop 
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

    

buttonList = []
for i in range(len(keys)):  
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))

# myButton = Button([100,100],"Q")
# myButton1 = Button([100,100],"Q")
# myButton2 = Button([100,100],"Q")

while True:
    success , img = cap.read()
    
    img = detector.findHands(img)   # Find the hands
    lmList, bboxInfo  = detector.findPosition(img)      # Font the land-mark points

    # for only one button
    # cv2.rectangle(img, (100,100),(200,200),(255,0,255),cv2.FILLED)
    # cv2.putText(img, "Q",(115,180),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
    # mybutton = Button([100,100],"Q")            #only for one button "Q"

    img = drawAll(img,buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            #finger-tip ko get krne k lia -->8 is the mediapipe number of finger-tip
            if x < lmList[8][0] < x+w  and y < lmList[8][1] < y+h:
                #hr button k arroud rectangle bna hua show krega
                cv2.rectangle(img, button.pos, (x+w,y+h), (175,0,175), cv2.FILLED)
                cv2.putText(img, button.text, (x+20, y+65) , cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                # if the distance between no. -8  and 12 is very small then it means it is click otherthan it is not click.
                l,_,_ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                # when clicked
                if l < 30 :
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x+w,y+h), (0,255,0), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65) , cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                    finalText += button.text
                    sleep(0.15)

    #this will give us the text 
    cv2.rectangle(img, (50,350), (700,450), (175,0,175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430) , cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 5)
                            


    cv2.imshow("Image",img)
    cv2.waitKey(1)




    # RESOURCES
    # 1.    https://www.youtube.com/watch?v=jzXZVFqEE2I
    # 2.    https://www.analyticsvidhya.com/blog/2021/09/develop-a-virtual-keyboard-using-opencv/
