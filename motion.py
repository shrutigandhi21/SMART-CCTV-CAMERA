# import cv2 
# def noise(self):
#     pass

import cv2 
import winsound

def noise():
    cam = cv2.VideoCapture(0)

    while cam.isOpened():
        retrive, frame1 = cam.read()
        retrive, frame2 = cam.read()
        
        #to get the difference if there is motion
        diff = cv2.absdiff(frame1, frame2)

        # this will change the video to gray color 
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # this will blur the video quality
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # this will sharpen the video quality
        _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # to detect something moving on the screen
        dilated = cv2.dilate(threshold, None, iterations=3)
        # the boundaries of the objects
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        # the next live will detect every small movements so to get only bigger movements we use the for loop 
        # cv2.drawContours(frame1, contours, -1, (0,255,0), 2)

        # to get the movements which are bigger
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h =cv2.boundingRect(c)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)
            
            winsound.Beep(500, 200)
            # winsound.PlaySound()

        if cv2.waitKey(10) == ord('q'):
            break

        cv2.imshow("Group 10's security camera", frame1)
        
    print("code completed")
        
    # cap = cv2.VideoCapture(0)

    # while True:
    #     _, frame1 = cap.read()
    #     _, frame2 = cap.read()

    #     diff = cv2.absdiff(frame2, frame1)
    #     diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    #     diff = cv2.blur(diff, (5,5))
    #     _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    #     contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    #     if len(contr) > 0:
    #         max_cnt = max(contr, key=cv2.contourArea)
    #         x,y,w,h = cv2.boundingRect(max_cnt)
    #         cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
    #         cv2.putText(frame1, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
    #         winsound.Beep(500, 200)

    #     else:
    #         cv2.putText(frame1, "NO-MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

    #     cv2.imshow("esc. to exit", frame1)

    #     if cv2.waitKey(1) == 27:
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         break