import numpy as np
import cv2

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def draw_circle(image, x, y, radius, color):
    cv2.circle(image, (int(x), int(y)), radius, color, -1)

def calculate_moving_average(value, window_size, value_list):
    value_list.append(value)
    if len(value_list) > window_size:
        value_list.pop(0)
    return sum(value_list) / len(value_list)