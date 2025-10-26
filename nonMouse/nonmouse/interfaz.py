# Contiene la pantalla de bienvenida
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from .selector import main_selector

# Función que se ejecutará al hacer clic en el botón "Iniciar todo"
def iniciar_aplicacion(window):
    #messagebox.showinfo("SkillPointer", "Iniciando la aplicación...")
    window.destroy()
    main_selector()
def main_interfaz():
    ventana = tk.Tk()
    ventana.title(" RehabilitacionJugando Featuring multi-movement activities")
    ventana.geometry("500x300")  # Tamaño de la ventana
    ventana.config(bg="#2c3e50")  # Color de fondo oscuro para un aspecto modern
    # Configuración del título en la ventana
    titulo = tk.Label(
        ventana,
        text="RehabilitacionJugando",
        font=("Helvetica", 24, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50"
    )
    titulo.pack(pady=20)  # Espacio alrededor del título
    # Configuración de la descripción en la ventana
    descripcion = tk.Label(
        ventana,
        text="Potenciando la motricidad fina y rehabilitacion en quienes lo necesitan",
        font=("Helvetica", 12),
        fg="#bdc3c7",
        bg="#2c3e50",
        wraplength=400,  # Limita el ancho de la descripción
        justify="center"
    )
    descripcion.pack(pady=10)
    # Configuración del botón de inicio
    boton_iniciar = tk.Button(
        ventana,
        text="Iniciar",
        font=("Helvetica", 14, "bold"),
        fg="#2c3e50",
        bg="#1abc9c",
        activebackground="#16a085",  # Color al hacer clic
        activeforeground="#ecf0f1",
        relief="flat",  # Quita los bordes para un estilo más moderno
        cursor="hand2",  # Cambia el cursor al pasar el mouse
        command=lambda:iniciar_aplicacion(ventana)
    )
    boton_iniciar.pack(pady=30)
# Inicia el bucle principal de la ventana
    ventana.mainloop()
    