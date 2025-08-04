import tkinter as tk
import ttkbootstrap as ttk

def on_click():
    print("El botón se ha pulsado")

# Crea la ventana
root = tk.Tk()

# Crea el botón
button = ttk.Button(root, bootstyle="primary", text="Pulse aquí", command=on_click)

# Coloca el botón en la ventana
button.pack()

# Inicia la aplicación
root.mainloop()