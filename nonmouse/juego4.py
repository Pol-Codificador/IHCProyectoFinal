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
def mostrar_instrucciones():
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
        set_game_active(4)

        iniciar_musica_juego4()

        game_window = GameWindow("Juego 4: Pellizca el Insecto")
        game_window.setGameFrame(logicaJuego4)
        game_window.run()

    tk.Button(root, text="Comenzar", command=continuar).pack(pady=20)

    root.mainloop()


# ----------- LÓGICA PRINCIPAL DEL JUEGO -------------
def logicaJuego4(game_frame):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondo.jpg")
    ruta_insecto = os.path.join(base_dir, "..", "images", "juego4", "insecto.png")

    # ---------------- FONDO ----------------
    fondo = cargar_imagen(ruta_fondo, altura=800)
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        game_frame.image = fondo

    # ---------------- BOTÓN REGRESAR ----------------
    def regresar_menu():
        from .selector import main_selector  # IMPORT LOCAL = NO CIRCULAR
        detener_musica()
        ventana = game_frame.winfo_toplevel()
        ventana.destroy()
        main_selector()

    boton_regresar = tk.Button(
        game_frame,
        text="Regresar al menú",
        font=("Arial", 12, "bold"),
        bg="#ff4d4d",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=regresar_menu
    )
    boton_regresar.place(x=20, y=70)

    # ---------------- PUNTAJE ----------------
    puntaje = tk.IntVar(value=0)
    label_puntaje = tk.Label(game_frame, text="Puntaje: 0", font=("Arial", 14), bg="#ffffff")
    label_puntaje.place(x=20, y=20)

    insectos = []

    # ---------------- CREAR INSECTO ----------------
    def crear_insecto():
        if get_game_active() != 4:
            return

        insecto_img = cargar_imagen(ruta_insecto, altura=100)

        if insecto_img:
            x = random.randint(100, 900)
            y = random.randint(150, 600)
            insecto = tk.Label(game_frame, image=insecto_img, borderwidth=0, highlightthickness=0, bg="#ffffff")
            insecto.image = insecto_img
            insecto.place(x=x, y=y)

            insectos.append((insecto, x, y))

            # --> El insecto desaparece tras 2 segundos
            def desaparecer():
                if (insecto, x, y) in insectos:
                    insecto.destroy()
                    insectos.remove((insecto, x, y))

            game_frame.after(2000, desaparecer)

        game_frame.after(2500, crear_insecto)

    crear_insecto()

    # ---------------- DETECTAR PELLIZCO ----------------
    def detectar_pellizco(event=None):
        if not insectos:
            return

        mouse_x = game_frame.winfo_pointerx() - game_frame.winfo_rootx()
        mouse_y = game_frame.winfo_pointery() - game_frame.winfo_rooty()

        for (insecto, x, y) in insectos[:]:
            if abs(mouse_x - x) < 80 and abs(mouse_y - y) < 80:
                insecto.destroy()
                insectos.remove((insecto, x, y))
                puntaje.set(puntaje.get() + 1)
                label_puntaje.config(text=f"Puntaje: {puntaje.get()}")

    game_frame.detectar_pellizco = detectar_pellizco
