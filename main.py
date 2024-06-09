import cv2
import numpy as np

# Detect edges using Canny edge detection
def cannyEdgeDetector(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edged = cv2.Canny(blurred, 155, 300)
    return edged

# Get region of interest by making a triangular mask and applying it to the edge image
def getROI(image):
    height, width = image.shape
    triangle = np.array([[(100, height), (width, height), (width - 360, int(height / 2))]])
    black_image = np.zeros_like(image)
    mask = cv2.fillPoly(black_image, triangle, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# Obtain approximate lines in the ROI with HoughLines method
def getLines(image):
    lines = cv2.HoughLinesP(image, 0.9, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=10)
    return lines

# Obtain coordinates of a line
def getLineCoordinatesFromParameters(image, line_parameters):
    slope = line_parameters[0]
    intercept = line_parameters[1]
    y1 = image.shape[0]
    y2 = int(y1 * (2.7 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

# Get the average value of the left and the right lines
def getSmoothLines(image, lines):
    left_fit = []
    right_fit = []

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    if left_fit:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = getLineCoordinatesFromParameters(image, left_fit_average)
    else:
        left_line = None

    if right_fit:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = getLineCoordinatesFromParameters(image, right_fit_average)
    else:
        right_line = None

    return np.array([left_line, right_line]) if left_line is not None and right_line is not None else None

# Display lines on the image
def displayLines(image, lines):
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return image

cap = cv2.VideoCapture('Drivings.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.namedWindow('Hough Transform', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hough Transform', 365, 650)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cannyEdgeDetector(gray)
    roi = getROI(canny)
    lines = getLines(roi)
    cv2.namedWindow('roi', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('roi', 365, 650)
    cv2.imshow('roi', roi)

    if lines is not None:
        smooth_lines = getSmoothLines(frame, lines)
        smoothlines_image = displayLines(frame, smooth_lines)
    else:
        smoothlines_image = frame

    cv2.imshow('Hough Transform', smoothlines_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
