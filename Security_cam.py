import cv2
import winsound

# to capture the video and 0 is the number of camera we will use 1 if we have multiple camera 
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

    if cv2.waitKey(10) == 27:
        break

    cv2.imshow("Group 10'ssecurity camera", frame1)
    
print("code completed")