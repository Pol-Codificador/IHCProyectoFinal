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
    root.title("Instrucciones - Pellizca los numeros")
    root.geometry("370x450")

    tk.Label(root, text='INSTRUCCIONES', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(
        root,
        text='Pellizca los numeros que llegaran de derecha a izquierda \n'
             'Cada numero eliminado suma puntos.',
        wraplength=300
    ).pack(pady=20)

    def continuar():
        root.destroy()
        set_game_active(2)

        iniciar_musica_juego2()

        game_window = GameWindow("Juego 2: Pellizca los numeros")
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

    # ---------------- ESTADÍSTICAS ----------------
    puntaje = tk.IntVar(value=0)
    vidas = tk.IntVar(value=5)

    stats_frame = tk.Frame(
        game_frame,
        bg=COLOR_CARD,
        highlightbackground="#dfe6e9",
        highlightthickness=2,
        bd=0
    )
    stats_frame.place(x=20, y=20, width=260, height=50)

    label_puntaje = tk.Label(
        stats_frame,
        text="Puntaje: 0",
        font=("Segoe UI", 14, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT,
        padx=10
    )
    label_puntaje.place(x=10, y=10)

    label_vidas = tk.Label(
        stats_frame,
        text="Vidas: 5",
        font=("Segoe UI", 14, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT,
        padx=10
    )
    label_vidas.place(x=135, y=10)

    # ---------------- LISTA DE NÚMEROS ----------------
    numeros = []

    # ---------------- CARGAR IMÁGENES (MEJORADO) ----------------
    from PIL import Image, ImageTk

    number_images = {}
    for i in range(10):
        ruta = os.path.join(base_dir, "..", "images", "juego2", f"{i}.png")
        try:
            img_pil = Image.open(ruta).convert("RGBA")

            # ======== LIMPIEZA AUTOMÁTICA DEL FONDO CUADRICULADO ========
            datas = img_pil.getdata()
            new_data = []
            for pixel in datas:
                r, g, b, a = pixel
                if r > 220 and g > 220 and b > 220:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(pixel)
            img_pil.putdata(new_data)
            # =============================================================

            img_pil = img_pil.resize((90, 90), Image.LANCZOS)
            number_images[i] = ImageTk.PhotoImage(img_pil)
        except:
            number_images[i] = None

    # ---------------- CREAR NÚMERO ----------------
    def crear_numero():
        if get_game_active() != 2:
            return

        valor = random.randint(0, 9)
        img = number_images[valor]
        if img is None:
            return

        x = 900
        y = random.randint(150, 600)

        label = tk.Label(
            game_frame,
            image=img,
            bg="#ffffff",
            highlightthickness=0,
            bd=0
        )
        label.image = img
        label.place(x=x, y=y)

        numeros.append({"widget": label, "x": x, "y": y, "valor": valor})

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

    # ---------------- DETECCIÓN DE CLICK ----------------
    def detectar_pellizco(event=None):
        mouse_x = game_frame.winfo_pointerx() - game_frame.winfo_rootx()
        mouse_y = game_frame.winfo_pointery() - game_frame.winfo_rooty()

        for num in numeros[:]:
            if abs(mouse_x - num["x"]) < 45 and abs(mouse_y - num["y"]) < 45:
                num["widget"].destroy()
                numeros.remove(num)

                puntaje.set(puntaje.get() + 1)
                label_puntaje.config(text=f"Puntaje: {puntaje.get()}")

    game_frame.detectar_pellizco = detectar_pellizco

    # ---------------- INICIAR JUEGO ----------------
    game_frame.after(500, crear_numero)
    mover_numeros()


