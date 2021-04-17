import cv2 
import numpy as np
from process import colour_slicing

global clickedBabe
clickedBabe = False

def capture_x_y(event, x, y, flags,param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clickedBabe
        clickedBabe = True
        print(x, y)
        mouseX, mouseY = x, y

def camera_loop(shared):
    cap = cv2.VideoCapture(-1)
    
    cv2.namedWindow('camera')
    cv2.setMouseCallback('camera',capture_x_y)
    
    global clickedBabe 
    clickedBabe = False
    while shared.mode_camera: #and not self.stopEvent_camera.is_set():
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.normalize(frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        
        if shared.start == True:
            frame = colour_slicing(frame, shared.colours, float(shared.radius.get()), beautify=shared.beautify, cube=shared.cube,
                                     width_p=int(shared.width_frame.get()), height_p=int(shared.height_frame.get()), positions=shared.position_click)
        # Display the resulting frame
        cv2.imshow('camera', frame)
        
        if 'mouseY' in globals() and 'clickedBabe' in globals():
            if clickedBabe:
                positions = (mouseY, mouseX)
                copy_colour = np.copy(frame[mouseY, mouseX])
                clickedBabe = False

        k = cv2.waitKey(2) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('a') and 'positions' in locals() and 'clickedBabe' in globals():
            shared.position_click = positions
            shared.colours = copy_colour
            print(shared.position_click, shared.colours)

        """
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif 0xFF == ord('a'):
            print(mouseX, mouseY)
        """

    # When everything done, release the capture
    shared.mode_camera = False
    cap.release()
    cv2.waitKey(200)
    cv2.destroyAllWindows()
    cv2.waitKey(500)


def video_loop(shared, path):
    cap = cv2.VideoCapture(path)
    
    cv2.namedWindow('video')
    cv2.setMouseCallback('video',capture_x_y)
    
    global clickedBabe 
    clickedBabe = False
    
    while cap.isOpened() and shared.mode_video:
        
        ret, frame = cap.read()
        frame = cv2.normalize(frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        if shared.start == True:
            frame = colour_slicing(frame, shared.colours, float(shared.radius.get()), beautify=shared.beautify, cube=shared.cube, 
                                     width_p=int(shared.width_frame.get()), height_p=int(shared.height_frame.get()), positions=shared.position_click)
        # Display the resulting frame
        
        cv2.imshow('video', frame)
        
        if 'mouseY' in globals() and 'clickedBabe' in globals():
            if clickedBabe:
                positions = (mouseY, mouseX)
                copy_colour = np.copy(frame[mouseY, mouseX])
                clickedBabe = False

        k = cv2.waitKey(2) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('a') and 'positions' in locals() and 'clickedBabe' in globals():
            shared.position_click = positions
            shared.colours = copy_colour
            print(shared.position_click, shared.colours)


    shared.mode_video = False
    cap.release()
    cv2.waitKey(200)
    cv2.destroyAllWindows()
    cv2.waitKey(500)
