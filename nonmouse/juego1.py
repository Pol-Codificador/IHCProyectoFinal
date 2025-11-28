import tkinter as tk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen
from .datosGlobales import set_game_active, get_game_active
import pygame


# ---------------- MÚSICA -----------------
def iniciar_musica_juego4():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_musica = os.path.join(base_dir, "..", "sonido", "Graze the Roof.mp3")

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Error al cargar música:", e)


def detener_musica():
    try:
        pygame.mixer.music.stop()
    except:
        pass


# ---------- FUNCIÓN PARA REGRESAR AL MENÚ (NUEVA) ----------
def regresar_menu(ventana):
    from .selector import main_selector  # ← IMPORT LOCAL (NO CREA CIRCULAR)
    detener_musica()
    ventana.destroy()
    main_selector()

# --------------- INSTRUCCIONES ----------------
def mostrar_instrucciones_juego1():
    root = tk.Tk()
    root.title("Instrucciones - Dibuja las letras")
    root.geometry("370x450")

    tk.Label(root, text='INSTRUCCIONES', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(
        root,
        text='Pellizca los puntos dibujando las formas que se pida para completar las letras',
        wraplength=300
    ).pack(pady=20)

    def continuar():
        root.destroy()
        set_game_active(4)

        # AQUÍ DEBE IR LA MÚSICA (antes del juego)
        iniciar_musica_juego4()

        game_window = GameWindow("Juego 1: Dibuja las letras")
        game_window.setGameFrame(logicaJuego1)
        game_window.run()

    tk.Button(root, text="Comenzar", command=continuar).pack(pady=20)

    root.mainloop()


# ----------- LÓGICA PRINCIPAL DEL JUEGO -------------
def logicaJuego1(game_frame):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego1", "fondo.png")
    ruta_punto = os.path.join(base_dir, "..", "images", "juego1", "punto.png")

    # ---------------- FONDO (CORREGIDO) ----------------
    fondo = cargar_imagen(ruta_fondo, altura=800)
    if fondo:
        game_frame.label_fondo = tk.Label(game_frame, image=fondo)
        game_frame.label_fondo.image = fondo     
        game_frame.label_fondo.place(relwidth=1, relheight=1)

    # ---------- BOTÓN REGRESAR AL MENÚ (NUEVO) ----------
    boton_regresar = tk.Button(
        game_frame,
        text="Regresar al menú",
        font=("Arial", 12, "bold"),
        bg="#2C3E50",
        fg="white",
        activebackground="#34495E",
        relief="flat",
        cursor="hand2",
        command=lambda: regresar_menu(game_frame.winfo_toplevel())
    )
    boton_regresar.place(x=20, y=20)
    # ----------------------------------------------------

    # --------- Variables de control ----------
    vocales = ["A", "E", "I", "O", "U"]
    indice_vocal = 0

    puntos = []  # (label, x, y)
    puntaje = tk.IntVar(value=0)

    label_vocal = tk.Label(
        game_frame,
        text=f"Vocal: {vocales[indice_vocal]}",
        font=("Arial", 30, "bold"),
        bg="#ffffff"
    )
    label_vocal.place(x=450, y=20)

    # ------------------ COORDENADAS DE CADA VOCAL ------------------
    def obtener_puntos_vocal(vocal):
        if vocal == "A":
            return [
                (450, 120),
                (420, 180), (480, 180),
                (400, 240), (500, 240),
                (380, 300), (520, 300),
                (360, 360), (540, 360),
                (420, 260), (450, 260), (480, 260)
            ]

        if vocal == "E":
            return [
                (400,120),(400,170),(400,220),(400,270),(400,320),
                (450,120),(480,120),
                (450,220),(480,220),
                (450,320),(480,320)
            ]

        if vocal == "I":
            return [
                (430,120),(450,120),(470,120),
                (450,170),(450,220),(450,270),(450,320),
                (430,320),(470,320)
            ]

        if vocal == "O":
            return [
                (420,150),(480,150),
                (380,200),(520,200),
                (360,250),(540,250),
                (380,300),(520,300),
                (420,350),(480,350)
            ]
        if vocal == "U":
            return [
                (380,150),(380,200),(380,250),(380,300),
                (520,150),(520,200),(520,250),(520,300),
                (400,340),(450,360),(500,340)
            ]

    # ------------------ GENERAR PUNTOS ------------------
    def dibujar_vocal():
        nonlocal puntos, indice_vocal

        for (lbl, _, _) in puntos:
            lbl.destroy()
        puntos.clear()

        coords = obtener_puntos_vocal(vocales[indice_vocal])
        punto_img = cargar_imagen(ruta_punto, altura=25)

        for (x, y) in coords:
            lbl = tk.Label(game_frame, image=punto_img, bg="#ffffff", borderwidth=0)
            lbl.image = punto_img
            lbl.place(x=x, y=y)
            puntos.append((lbl, x, y))

    dibujar_vocal()

    # ---------------- DETECTAR "PELLIZCO" ----------------
    def detectar_pellizco(event=None):
        nonlocal indice_vocal, puntos

        if not puntos:
            return

        mouse_x = game_frame.winfo_pointerx() - game_frame.winfo_rootx()
        mouse_y = game_frame.winfo_pointery() - game_frame.winfo_rooty()

        for (lbl, x, y) in puntos[:]:
            if abs(mouse_x - x) < 40 and abs(mouse_y - y) < 40:
                lbl.destroy()
                puntos.remove((lbl, x, y))
                puntaje.set(puntaje.get() + 1)

        # --------- ¿Se terminó la vocal? pasar a la siguiente ---------
        if len(puntos) == 0:
            indice_vocal += 1
            if indice_vocal >= len(vocales):
                indice_vocal = 0

            label_vocal.config(text=f"Vocal: {vocales[indice_vocal]}")
            dibujar_vocal()

    game_frame.detectar_pellizco = detectar_pellizco
