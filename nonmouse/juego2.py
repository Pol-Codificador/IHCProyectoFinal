import tkinter as tk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen
from .datosGlobales import set_game_active, get_game_active
import pygame


# ---------------- MÚSICA -----------------
def iniciar_musica_juego2():
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
def mostrar_instrucciones2():
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
        set_game_active(2)

        iniciar_musica_juego2()

        game_window = GameWindow("Juego 2: Pellizca el Insecto")
        game_window.setGameFrame(logicaJuego2)
        game_window.run()

    tk.Button(root, text="Comenzar", command=continuar).pack(pady=20)

    root.mainloop()
    
    # ----------- LÓGICA PRINCIPAL DEL JUEGO -------------
def logicaJuego2(game_frame):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # ---------------- FONDO ----------------
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego2", "fondo.png")
    fondo = cargar_imagen(ruta_fondo, altura=800)
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        label_fondo.lower()
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

    # ---------------- ESTADÍSTICAS ----------------
    puntaje = tk.IntVar(value=0)
    vidas = tk.IntVar(value=5)

    label_puntaje = tk.Label(game_frame, text="Puntaje: 0", font=("Arial", 14), bg="#ffffff")
    label_puntaje.place(x=20, y=20)

    label_vidas = tk.Label(game_frame, text="Vidas: 5", font=("Arial", 14), bg="#ffffff")
    label_vidas.place(x=150, y=20)

    # ---------------- LISTA DE NÚMEROS ----------------
    numeros = []

    # ---------------- CARGAR IMÁGENES DE NÚMEROS ----------------
    number_images = {}
    for i in range(10):
        ruta = os.path.join(base_dir, "..", "images", "juego2", f"{i}.png")
        try:
            img_pil = Image.open(ruta)
            img_pil = img_pil.resize((80, 80), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img_pil)
            number_images[i] = img
        except Exception as e:
            print(f"Error cargando {ruta}: {e}")
            number_images[i] = None

    # ---------------- CREAR NÚMERO ----------------
    def crear_numero():
        if get_game_active() != 2:
            return

        valor = random.randint(0, 9)
        img = number_images[valor]

        if img is None:
            return  # si no cargó, saltar

        x = 900 

        y = random.randint(150, 600)

        label = tk.Label(game_frame, image=img, bg="#ffffff")
        label.image = img
        label.place(x=x, y=y)

        numeros.append({
            "widget": label,
            "x": x,
            "y": y,
            "valor": valor
        })

        game_frame.after(700, crear_numero)

    # ---------------- MOVER NÚMEROS ----------------
    def mover_numeros():
        if get_game_active() != 2:
            return

        for num in numeros[:]:
            num["x"] -= 6
            num["widget"].place(x=num["x"], y=num["y"])

            if num["x"] <= 40:
                num["widget"].destroy()
                numeros.remove(num)

                vidas.set(vidas.get() - 1)
                label_vidas.config(text=f"Vidas: {vidas.get()}")

                if vidas.get() <= 0:
                    detener_musica()
                    tk.messagebox.showinfo("Juego terminado", "Te quedaste sin vidas!")
                    regresar_menu()
                    return

        game_frame.after(40, mover_numeros)

    # ---------------- DETECTAR PELLIZCO / CLICK ----------------
    def detectar_pellizco(event=None):
        mouse_x = game_frame.winfo_pointerx() - game_frame.winfo_rootx()
        mouse_y = game_frame.winfo_pointery() - game_frame.winfo_rooty()

        for num in numeros[:]:
            if abs(mouse_x - num["x"]) < 40 and abs(mouse_y - num["y"]) < 40:
                num["widget"].destroy()
                numeros.remove(num)

                puntaje.set(puntaje.get() + 1)
                label_puntaje.config(text=f"Puntaje: {puntaje.get()}")

    game_frame.detectar_pellizco = detectar_pellizco

    # ---------------- INICIAR JUEGO ----------------
    game_frame.after(500, crear_numero)
    mover_numeros()

