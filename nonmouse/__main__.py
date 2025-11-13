"""No se esta utilizando"""
import cv2
import time
import keyboard
import platform
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller
from nonmouse.args import *
from nonmouse.utils import *
from .datosGlobales import get_game_active 

mouse = Controller()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pf = platform.system()
if pf == 'Windows':
    hotkey = 'Alt'
elif pf == 'Darwin':
    hotkey = 'Command'
elif pf == 'Linux':
    hotkey = 'XXX'              # La tecla de acceso rápido está deshabilitada en Linux
def main():
    print("main : El valor de juego activo es  : ")
    print(get_game_active())
    
    cap_device, mode, kando, screenRes = tk_arg()
    dis = 0.7                           # Definición de la distancia para pegar
    preX, preY = 0, 0
    nowCli, preCli = 0, 0               # Estado actual y previo del clic izquierdo
    norCli, prrCli = 0, 0               # Estado actual y previo del clic derecho
    douCli = 0                          # Estado de doble clic
    i, k, h = 0, 0, 0
    LiTx, LiTy, list0x, list0y, list1x, list1y, list4x, list4y, list6x, list6y, list8x, list8y, list12x, list12y = [
    ], [], [], [], [], [], [], [], [], [], [], [], [], []   # Listas para el promedio móvil
    moving_average = [[0] * 3 for _ in range(3)]
    nowUgo = 1
    cap_width = 1280
    cap_height = 720
    start, c_start = float('inf'), float('inf')
    c_text = 0
    # Entrada de la cámara web, configuración
    window_name = 'Configuración de Camara'
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cfps = int(cap.get(cv2.CAP_PROP_FPS))
    if cfps < 30:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
        cfps = int(cap.get(cv2.CAP_PROP_FPS))
    # Cantidad de suavizado (menor: el cursor se mueve con más frecuencia, mayor: mayor retraso)
    ran = max(int(cfps / 10), 1)
    hands = mp_hands.Hands(
        min_detection_confidence=0.8,   # Confianza en la detección
        min_tracking_confidence=0.8,    # Confianza en el seguimiento
        max_num_hands=1                 # Número máximo de manos detectadas
    )
    # Bucle principal ###############################################################################
    while cap.isOpened():
        p_s = time.perf_counter()
        success, image = cap.read()
        if not success:
            continue
        if mode == 1:                   # Mouse
            image = cv2.flip(image, 0)  # Voltear verticalmente
        elif mode == 2:                 # Touch
            image = cv2.flip(image, 1)  # Voltear horizontalmente

        # Voltear la imagen horizontalmente y convertir de BGR a RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False   # Marcar la imagen como no escribible para pasar por referencia
        results = hands.process(image)  # Procesamiento con mediapipe
        image.flags.writeable = True    # Dibujar las anotaciones de las manos en la imagen
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks:
            # Dibujo de la estructura ósea de la mano
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if pf == 'Linux':           # Si es Linux, mover siempre
                can = 1
                c_text = 0
            else:                       # Si no es Linux, aceptar entradas desde el teclado
                if keyboard.is_pressed(hotkey):  # En Linux no se debe entrar en esta condición
                    can = 1
                    c_text = 0          # Sin presionar la tecla de acceso rápido
                else:                   # Si no hay entrada, no mover
                    can = 0
                    c_text = 1          # Con tecla de acceso rápido presionada
                    # i = 0
            # Cuando la tecla de acceso rápido global está presionada ##################################################
            if can == 1:
                # print(hand_landmarks.landmark[0])
                # Asignar la posición actual del mouse a preX, preY, se ejecuta solo una vez
                if i == 0:
                    preX = hand_landmarks.landmark[8].x
                    preY = hand_landmarks.landmark[8].y
                    i += 1

                # Cálculo del promedio móvil de las coordenadas de los puntos de referencia utilizados a continuación
                landmark0 = [calculate_moving_average(hand_landmarks.landmark[0].x, ran, list0x), calculate_moving_average(
                    hand_landmarks.landmark[0].y, ran, list0y)]
                landmark1 = [calculate_moving_average(hand_landmarks.landmark[1].x, ran, list1x), calculate_moving_average(
                    hand_landmarks.landmark[1].y, ran, list1y)]
                landmark4 = [calculate_moving_average(hand_landmarks.landmark[4].x, ran, list4x), calculate_moving_average(
                    hand_landmarks.landmark[4].y, ran, list4y)]
                landmark6 = [calculate_moving_average(hand_landmarks.landmark[6].x, ran, list6x), calculate_moving_average(
                    hand_landmarks.landmark[6].y, ran, list6y)]
                landmark8 = [calculate_moving_average(hand_landmarks.landmark[8].x, ran, list8x), calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, list8y)]
                landmark12 = [calculate_moving_average(hand_landmarks.landmark[12].x, ran, list12x), calculate_moving_average(
                    hand_landmarks.landmark[12].y, ran, list12y)]

                # Distancia de referencia entre los puntos relativos de los dedos, luego dividir las distancias obtenidas de mediapipe por este valor
                absKij = calculate_distance(landmark0, landmark1)
                # Distancia euclidiana entre la punta del dedo índice y la punta del dedo medio
                absUgo = calculate_distance(landmark8, landmark12) / absKij
                # Distancia euclidiana entre la segunda articulación del dedo índice y la punta del pulgar
                absCli = calculate_distance(landmark4, landmark6) / absKij

                posx, posy = mouse.position

                # Mapear la punta del dedo índice al cursor
                # Convertir las coordenadas de la cámara en el movimiento del mouse
                nowX = calculate_moving_average(
                    hand_landmarks.landmark[8].x, ran, LiTx)
                nowY = calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, LiTy)

                dx = kando * (nowX - preX) * image_width
                dy = kando * (nowY - preY) * image_height

                if pf == 'Windows' or pf == 'Linux':     # En Windows o Linux, ajustar el movimiento del mouse sumando 0.5
                    dx = dx + 0.5
                    dy = dy + 0.5
                preX = nowX
                preY = nowY
                # print(dx, dy)
                if posx + dx < 0:  # Evitar que el cursor se salga de la pantalla y no vuelva

                    dx = -posx
                elif posx+dx > screenRes[0]:
                    dx = screenRes[0]-posx
                if posy+dy < 0:
                    dy = -posy
                elif posy+dy > screenRes[1]:
                    dy = screenRes[1]-posy

                # Flags #########################################################################
                # Estado de clic
                if absCli < dis:
                    nowCli = 1          # nowCli: estado del clic izquierdo (1: clic  0: no clic)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 250, 250))
                elif absCli >= dis:
                    nowCli = 0
                if np.abs(dx) > 7 and np.abs(dy) > 7:
                    k = 0                           # Cuando "está en movimiento", k = 0
                # Estado del clic derecho: si el clic dura más de 1 segundo y el cursor no se mueve
                # Cuando no se mueve y se hace clic
                if nowCli == 1 and np.abs(dx) < 7 and np.abs(dy) < 7:
                    if k == 0:          # k: estado de clic y el cursor no se está moviendo. k = 0 se establece en las líneas 113 y 140
                        start = time.perf_counter()
                        k += 1
                    end = time.perf_counter()
                    if end - start > 1.5:
                        norCli = 1
                        draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                    hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 250))
                else:
                    norCli = 0

                # Mover el cursor ###################################################################
                # cursor
                if absUgo >= dis and nowUgo == 1:
                    mouse.move(dx, dy)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 8, (250, 0, 0))
                # clic izquierdo
                if nowCli == 1 and nowCli != preCli:
                    if h == 1:                                  # Después de hacer clic derecho: no hacer clic izquierdo
                        h = 0
                    elif h == 0:                                # Estado normal
                        mouse.press(Button.left)
                    # print('Click')
                # Liberar clic izquierdo
                if nowCli == 0 and nowCli != preCli:
                    mouse.release(Button.left)
                    k = 0
                    # print('Release')
                    if douCli == 0:                             # Después del primer clic, medir el tiempo
                        c_start = time.perf_counter()
                        douCli += 1
                    c_end = time.perf_counter()
                    if 10 * (c_end - c_start) > 5 and douCli == 1:  # Si se hace otro clic dentro de 0.5 segundos, es un doble clic
                        mouse.click(Button.left, 2)             # doble clic
                        douCli = 0
                # clic derecho
                if norCli == 1 and norCli != prrCli:
                    # mouse.release(Button.left)                # Extrañamente necesario
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                    h = 1                                       # Después del clic derecho: h = 1
                    # print("right click")

                
                if get_game_active() == 4:  # Verifica si el juego activo es "game4"
                    # Detectar gesto de pellizco (distancia entre el pulgar e índice)
                    distancia_pellizco = calculate_distance(landmark4, landmark8)

                    # Definir un umbral para detectar el pellizco
                    umbral_pellizco = 0.05

                    # Verificar si ocurre el gesto de pellizco
                    if distancia_pellizco < umbral_pellizco:
                        # Realizar el clic derecho
                        mouse.press(Button.right)
                        mouse.release(Button.right)
                        draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                    hand_landmarks.landmark[8].y * image_height, 20, (255, 105, 180))  # Rosa
                        print("Clic derecho activado por el pellizco")
                
                # scroll
                if hand_landmarks.landmark[8].y-hand_landmarks.landmark[5].y > -0.06:
                    mouse.scroll(0, -dy/50)                     # スクロール感度下げる
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 0))
                    nowUgo = 0
                else:
                    nowUgo = 1

                preCli = nowCli
                prrCli = norCli

        # 表示 #################################################################################
        if c_text == 1:
            cv2.putText(image, f"Push {hotkey}", (20, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(image, "cameraFPS:"+str(cfps), (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        p_e = time.perf_counter()
        fps = str(int(1/(float(p_e)-float(p_s))))
        cv2.putText(image, "FPS:"+fps, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        dst = cv2.resize(image, dsize=None, fx=0.4,
                         fy=0.4)         # HDの0.4倍で表示
        cv2.imshow(window_name, dst)
        if (cv2.waitKey(1) & 0xFF == 27) or (cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == 0):
            break
    cap.release()
"""
if __name__ == "__main__":
    main()
"""