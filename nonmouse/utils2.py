#Funciones globales como cargar imagenes
import numpy as np
import cv2
from PIL import Image, ImageTk 
import os

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def draw_circle(image, x, y, radius, color):
    cv2.circle(image, (int(x), int(y)), radius, color, -1)

def calculate_moving_average(value, window_size, value_list):
    value_list.append(value)
    if len(value_list) > window_size:
        value_list.pop(0)
    return sum(value_list) / len(value_list)
def cargar_imagen(ruta, altura=None):
    try:
        imagen = Image.open(ruta)
        if altura:
            # Redimensionar la imagen manteniendo la relación de aspecto
            ancho = int(imagen.width * (altura / imagen.height))
            imagen = imagen.resize((ancho, altura), Image.ANTIALIAS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"No se pudo cargar la imagen desde {ruta}: {e}")
        return None
