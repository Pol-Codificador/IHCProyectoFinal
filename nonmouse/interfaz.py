import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
from .selector import main_selector

def iniciar_aplicacion(window):
    window.destroy()
    main_selector()

def main_interfaz():
    ventana = tk.Tk()
    ventana.title("RMNMouse")
    ventana.geometry("900x500")
    ventana.configure(bg="#0B173B")  # Azul oscuro base por si no carga el fondo

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        ruta_imagen = os.path.join(project_dir, "images", "fondo_imagen.png")

        imagen = Image.open(ruta_imagen)
        altura = 500
        ancho = int(imagen.width * (altura / imagen.height))
        imagen_redimensionada = imagen.resize((ancho, altura), Image.ANTIALIAS)
        fondo = ImageTk.PhotoImage(imagen_redimensionada)

        label_fondo = tk.Label(ventana, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        label_fondo.image = fondo
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")

    # Nuevo esquema de color
    fondo_frame = "#1E2A47"   # Azul más claro que el fondo general
    color_borde = "#304674"   # Azul grisáceo para borde
    color_texto = "#E8F1FF"   # Blanco azulado suave
    color_boton = "#3B6CF5"   # Azul vivo moderno
    color_boton_hover = "#2E54C6"

    frame_texto = tk.Frame(
        ventana,
        bg=fondo_frame,
        highlightbackground=color_borde,
        highlightthickness=3,
        width=400,
        height=230,
        padx=30,
        pady=20
    )
    frame_texto.place(relx=0.1, rely=0.5, anchor="w")

    try:
        ruta_imagen_titulo = os.path.join(project_dir, "images", "titulo.png")
        imagen_titulo = Image.open(ruta_imagen_titulo)
        imagen_titulo = imagen_titulo.resize((380, 90), Image.ANTIALIAS)
        imagen_titulo_tk = ImageTk.PhotoImage(imagen_titulo)

        label_titulo = tk.Label(frame_texto, image=imagen_titulo_tk, bg=fondo_frame)
        label_titulo.image = imagen_titulo_tk
        label_titulo.pack(pady=(5, 15))
    except Exception as e:
        print(f"No se pudo cargar la imagen del título: {e}")

    descripcion = tk.Label(
        frame_texto,
        text="Ayudando en la rehabilitación motora de los más peques",
        font=("Segoe UI", 12, "italic"),
        fg=color_texto,
        wraplength=360,
        bg=fondo_frame,
        justify="left"
    )
    descripcion.pack(pady=(0, 20), anchor="w")

    boton_iniciar = tk.Button(
        frame_texto,
        text="Iniciar",
        font=("Segoe UI Semibold", 16),
        fg="#FFFFFF",
        bg=color_boton,
        activebackground=color_boton_hover,
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=12,
        height=1,
        command=lambda: iniciar_aplicacion(ventana)
    )
    boton_iniciar.pack(pady=10, anchor="w")

    ventana.mainloop()

main_interfaz()