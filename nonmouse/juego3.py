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

    # ======================= ESTILOS ===========================
    COLOR_TEXT = "#2c3e50"
    COLOR_CARD = "#ffffff"
    COLOR_ACCENT = "#0984e3"
    COLOR_ACCENT_LIGHT = "#74b9ff"
    COLOR_DANGER = "#d63031"
    COLOR_DANGER_LIGHT = "#ff7675"

    # ---------------- BOTÓN REGRESAR ----------------
    def regresar_menu():
        from .selector import main_selector
        detener_musica()
        ventana = game_frame.winfo_toplevel()
        ventana.destroy()
        main_selector()

    tk.Button(
        game_frame,
        text="⟵ Volver",
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_DANGER,
        fg="white",
        activebackground=COLOR_DANGER_LIGHT,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=10,
        highlightthickness=0,
        command=regresar_menu
    ).place(x=20, y=70)

    # ---------------- TARJETA: PUNTAJE ----------------
    puntaje = tk.IntVar(value=0)

    stats_frame = tk.Frame(
        game_frame,
        bg=COLOR_CARD,
        highlightbackground="#dfe6e9",
        highlightthickness=2
    )
    stats_frame.place(x=20, y=20, width=180, height=50)

    label_puntaje = tk.Label(
        stats_frame,
        text="Puntaje: 0",
        font=("Segoe UI", 14, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    )
    label_puntaje.place(x=10, y=10)

    # ---------------- TARJETA: OBJETIVO ----------------
    objetivo_frame = tk.Frame(
        game_frame,
        bg=COLOR_CARD,
        highlightbackground="#dfe6e9",
        highlightthickness=2
    )
    objetivo_frame.place(x=350, y=20, width=450, height=60)

    label_objetivo = tk.Label(
        objetivo_frame,
        text="",
        font=("Segoe UI", 20, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    )
    label_objetivo.place(relx=0.5, rely=0.5, anchor="center")

    # ---------------- COLORES EN PANTALLA ----------------
    botones_colores = []

    def generar_colores():
        """Genera 3 colores nuevos y un objetivo."""
        for b, _, _ in botones_colores:
            b.destroy()
        botones_colores.clear()

        # 3 colores aleatorios
        elegidos = random.sample(colores_disponibles, 3)

        # Objetivo
        objetivo = random.choice(elegidos)
        label_objetivo.config(text=f"Selecciona: {objetivo.upper()}")

        # Coloca las imágenes
        for idx, color in enumerate(elegidos):
            ruta = os.path.join(base_dir, "..", "images", "juego3", f"{color}.png")

            # ======================================================
            #     🔥🔥 LIMPIEZA AUTOMÁTICA DEL FONDO CUADRICULADO 🔥🔥
            # ======================================================
            from PIL import Image, ImageTk

            img_raw = Image.open(ruta).convert("RGBA")
            datas = img_raw.getdata()
            new_data = []

            for pixel in datas:
                r, g, b, a = pixel
                # Si es casi blanco / gris → transparente
                if r > 220 and g > 220 and b > 220:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(pixel)

            img_raw.putdata(new_data)

            # Redimensionar manteniendo altura
            altura = 170
            w, h = img_raw.size
            ratio = altura / h
            img_raw = img_raw.resize((int(w * ratio), altura), Image.LANCZOS)

            img = ImageTk.PhotoImage(img_raw)
            # ======================================================

            # Centrado horizontal de los 3 colores
            game_width = game_frame.winfo_width()
            if game_width == 1:
                game_width = 1080  # fallback temporal

            total_width = 3 * 170 + 2 * 60
            start_x = (game_width - total_width) // 2
            y = 300

            x = start_x + idx * (170 + 60)

            lbl = tk.Label(game_frame, image=img, bg="#ffffff", borderwidth=0)
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
            if abs(mouse_x - x) < 110 and abs(mouse_y - y) < 110:
                if color == color_objetivo:
                    puntaje.set(puntaje.get() + 1)
                    label_puntaje.config(text=f"Puntaje: {puntaje.get()}")

                    # Nuevo set de colores
                    color_objetivo = generar_colores()

    # Conexión a la detección de pellizco desde la cámara
    game_frame.detectar_pellizco = detectar_pellizco
