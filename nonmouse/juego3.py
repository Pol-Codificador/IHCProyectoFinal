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


# --------------- INSTRUCCIONES ----------------
def mostrar_instrucciones3():
    root = tk.Tk()
    root.title("Instrucciones - Pellizca el insecto")
    root.geometry("370x450")

    tk.Label(root, text='INSTRUCCIONES', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(
        root,
        text='Pellizca los insectos con los dedos índice y pulgar para eliminarlos.\n'
             'Cada insecto eliminado suma puntos.',
        wraplength=300
    ).pack(pady=20)

    def continuar():
        root.destroy()
        set_game_active(3)

        iniciar_musica_juego4()

        game_window = GameWindow("Juego 3: Selecciona el color")
        game_window.setGameFrame(logicaJuego3)
        game_window.run()

    tk.Button(root, text="Comenzar", command=continuar).pack(pady=20)

    root.mainloop()


# ----------- LÓGICA PRINCIPAL DEL JUEGO -------------
def logicaJuego3(game_frame):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego3", "fondo.png")

    colores_disponibles = [
        "rojo", "azul", "verde",
        "amarillo", "morado", "naranja",
        "rosado", "blanco", "negro"
    ]

    # ---------------- FONDO ----------------
    fondo = cargar_imagen(ruta_fondo, altura=800)
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        game_frame.image = fondo

    # ---------------- BOTÓN REGRESAR ----------------
    def regresar_menu():
        from .selector import main_selector
        detener_musica()
        ventana = game_frame.winfo_toplevel()
        ventana.destroy()
        main_selector()

    tk.Button(
        game_frame,
        text="Regresar al menú",
        font=("Arial", 12, "bold"),
        bg="#ff4d4d",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=regresar_menu
    ).place(x=20, y=70)

    # ---------------- PUNTAJE ----------------
    puntaje = tk.IntVar(value=0)
    label_puntaje = tk.Label(game_frame, text="Puntaje: 0", font=("Arial", 14), bg="#ffffff")
    label_puntaje.place(x=20, y=20)

    # ---------------- TEXTO DE OBJETIVO ----------------
    label_objetivo = tk.Label(game_frame, text="", font=("Arial", 20, "bold"), bg="#ffffff")
    label_objetivo.place(x=400, y=20)

    # ---------------- COLORES EN PANTALLA ----------------
    botones_colores = []

    def generar_colores():
        """Genera 3 colores nuevos y un objetivo."""
        # Limpia los colores anteriores
        for b, _, _ in botones_colores:
            b.destroy()
        botones_colores.clear()

        # Selecciona 3 colores aleatorios
        elegidos = random.sample(colores_disponibles, 3)

        # Objetivo
        objetivo = random.choice(elegidos)
        label_objetivo.config(text=f"Selecciona: {objetivo.upper()}")

        # Crear los 3 colores como imágenes
        for idx, color in enumerate(elegidos):
            ruta = os.path.join(base_dir, "..", "images", "juego3", f"{color}.png")
            img = cargar_imagen(ruta, altura=150)

            x = 250 + idx * 220
            y = 300

            lbl = tk.Label(game_frame, image=img, bg="#ffffff")
            lbl.image = img
            lbl.place(x=x, y=y)

            botones_colores.append((lbl, color, (x, y)))

        return objetivo

    color_objetivo = generar_colores()

    # ---------------- DETECTAR PELLIZCO ----------------
    def detectar_pellizco(event=None):
        nonlocal color_objetivo

        mouse_x = game_frame.winfo_pointerx() - game_frame.winfo_rootx()
        mouse_y = game_frame.winfo_pointery() - game_frame.winfo_rooty()

        for (lbl, color, (x, y)) in botones_colores:
            if abs(mouse_x - x) < 100 and abs(mouse_y - y) < 100:
                if color == color_objetivo:
                    puntaje.set(puntaje.get() + 1)
                    label_puntaje.config(text=f"Puntaje: {puntaje.get()}")

                    # Generar nuevo set de colores
                    color_objetivo = generar_colores()

    # *** IMPORTANTE ***
    # Esto conecta este juego con la cámara SIN modificar baseJuego
    game_frame.detectar_pellizco = detectar_pellizco