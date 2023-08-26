import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math


# function to decide if point is inside nested rectangle
def isPointInsideMousePad(frameTopLeft:tuple,mousepadTopLeft:tuple, frameBottomRight:tuple,mousepadBottomRight:tuple, point:tuple):
    x, y = point
    x1, y1 = frameTopLeft
    x2, y2 = mousepadTopLeft
    x3, y3 = mousepadBottomRight
    x4, y4 = frameBottomRight
    if (x > x1) & (x > x2) & (x < x3) & (x < x4) & (y > y1) & (y > y2) & (y < y3) & (y < y4):
        return True
    else:
        return False


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode = True, min_detection_confidence=0.3, max_num_hands = 1)

screen_size = pyautogui.size() # Size(width=1920, height=1200)  --> size of screen
screen_width = screen_size.width
screen_height = screen_size.height

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    frameTopLeft = (0, 0)
    frameBottomRight = (frame_width, frame_height)
    mouse_track_pad_width, mouse_track_pad_height = frame_width/1.6, frame_height/1.6
    mousepadTopLeft = (int((frame_width - mouse_track_pad_width)/2), int((frame_height - mouse_track_pad_height)/2))
    mousepadBottomRight = (int(((frame_width - mouse_track_pad_width)/2) + mouse_track_pad_width), int(((frame_height - mouse_track_pad_height)/2) + mouse_track_pad_height))
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hands_results = hands.process(frame_RGB)
    #print(hands_results)

    if hands_results.multi_hand_landmarks: # if there is any hand detected then we go in for mouse functionality. else, we capture next frame
        for hand_landmarks in hands_results.multi_hand_landmarks: # we iterete over every hand that is detected in order to get it's landmarks....but we are tracking only 1 hand
            # uncomment below code to visualize the landmark points detected
            """ mp_drawing.draw_landmarks(
                    frame, # image to draw
                    hand_landmarks, # model output
                    mp_hands.HAND_CONNECTIONS, # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()) """
            # xi, yi are normalized coordinates for index finger tip
            xi = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            yi = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # xm, ym are normalized coords for middle finger tip
            xm = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
            ym = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

            # xt, yt are normalized coords for thumb tip
            xt = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            yt = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            # below line converts normalized coords to pixel coords w.r.to frame
            circle_origin_x, circle_origin_y = int(xi * frame_width), int(yi * frame_height)
            # below line converts pixel coords w.r.to frame ----> pixel coords w.r.to virtual mouse region 
            circle_origin_x1, circle_origin_y1 = int(circle_origin_x - mousepadTopLeft[0]), int(circle_origin_y - mousepadTopLeft[1])
            # below code converts pixel coord w.r.to virtual mouse region ---> pixel coords w.r.to screen
            circle_origin_x2, circle_origin_y2 = int(circle_origin_x1 * 4.8), int(circle_origin_y1 * 4)

            # we decide if the index finger tip is inside virtual mouse region or not
            pointInsideMousePad = isPointInsideMousePad(frameTopLeft, mousepadTopLeft, mousepadBottomRight, frameBottomRight, (circle_origin_x, circle_origin_y)) 
            if pointInsideMousePad: # if point is inside VMR (Virtual Mouse Region)
                # Now we calculate euclidian dist between index_finger_tip and middle_finger_tip to implement rightclick functionality

                if 0.00100 < round(math.dist([xi, yi], [xm, ym]), 5) < 0.03000:
                    pyautogui.rightClick(duration=0.2) # Clicks the Right Mouse Button

                # Now we calculate euclidian dist between index_finger_tip and thumb_tip to implement leftclick functionality.
                # if you hold your index finger and thumb together for 12ms then while loop goes to next frame and below code acts as double-click functionality
                # if you hold < 12ms then it works as single left click.

                elif 0.00100 < round(math.dist([xi, yi], [xt, yt]), 5) < 0.03000:
                    pyautogui.leftClick()    # Clicks the Left Mouse Button
                    cv2.waitKey(3)
                
                # else condition is to move the mouse pointer
                else:
                    cv2.circle(frame, (circle_origin_x, circle_origin_y), 10, (0, 255, 0), 2, cv2.LINE_AA)
                    pyautogui.moveTo(circle_origin_x2, circle_origin_y2, duration=0.1)
                
            # this condition is to check if index_finger_tip is outside the VMR. if it is outside then red circle is drawn
            else :
                cv2.circle(frame, (circle_origin_x, circle_origin_y), 10, (0, 0, 255), 2, cv2.LINE_AA)
    
    # code for drawing Virtual Mouse Region 
    cv2.rectangle(frame, mousepadTopLeft, mousepadBottomRight, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, 'Virtual Mouse Region', (120, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(15)

    # press Esc to quit the program.
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
