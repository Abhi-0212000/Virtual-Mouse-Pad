# Virtual-Mouse-Pad
## Virtual Mouse Pad using OpenCV, mediapipe and pyautogui

<h4>Follow this repository to implement your own __Virtual__ __Mouse__ __Pad__.</h4>

<h4>Overview of how this project is implemented:</h4>

1. We start capturing video and drawing the Virtual Mousepad Region on every frame.
2. If the hand is detected in the frame, we take landmark points of index finger tip, thumb tip, and middle fingertip.
3. We check if index fingertip is inside virtualMousePadRegion or not. If __YES__ then we go for mouse tracking with gesture functionality. If __NO__ then we read the next frame.
4. We implement logic to track the movement of index finger tip and we use that information to move mouse pointer.
5. We also implement logics for right click, left single click and left double click mouse functionalities.

Check out the images at the end of this file to understand the logic for coordinate transformations and other calculations used in code.

__Demo__ __Video__:



![coordinateSystem](https://github.com/Abhi-0212000/Virtual-Mouse-Pad/assets/70425157/7f696034-298d-4893-87e3-73de260b4723)
![calculations](https://github.com/Abhi-0212000/Virtual-Mouse-Pad/assets/70425157/75bb3542-bbcf-4475-ada1-4f7f69ea9c81)



