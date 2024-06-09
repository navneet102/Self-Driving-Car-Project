import cv2
import numpy as np

def detect_traffic_lights_in_video(video_path):
    # Open video capture
    cap = cv2.VideoCapture(video_path)
    
    while(cap.isOpened()):
        # Read frame from the video
        ret, frame = cap.read()
        
        if ret:
            # Convert frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define range of red color in HSV
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            
            # Threshold the HSV image to get only red colors
            mask_red = cv2.inRange(hsv, lower_red, upper_red)
            
            # Perform morphological operations to remove noise
            mask_red = cv2.erode(mask_red, None, iterations=2)
            mask_red = cv2.dilate(mask_red, None, iterations=2)
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Loop over the contours
            for contour in contours:
                # Approximate the contour to a circle
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                
                # If the contour is approximately a circle
                if len(approx) >= 6:
                    # Draw a bounding box around the traffic light
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display the frame with bounding boxes
            cv2.imshow('Traffic Lights Detection', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    # Release video capture
    cap.release()
    cv2.destroyAllWindows()


detect_traffic_lights_in_video('traffic/video.mp4')