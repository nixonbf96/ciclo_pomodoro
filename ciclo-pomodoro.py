import time
import os
from typing import Callable, Optional
from datetime import datetime, timedelta
import tkinter as tk
import ttkbootstrap as ttk
from win10toast import ToastNotifier
import threading

toaster = ToastNotifier()
root = tk.Tk()
root.attributes('-topmost', True)
root.title("Ciclo Pomodoro")
alto_ventana = 40
root.geometry(f"200x{alto_ventana}+0+0")

frame = ttk.Frame(root, bootstyle="info", padding=10)
frame.pack()
label_mensaje = ttk.Label(frame, text="", bootstyle='inverse-info')
label_mensaje.pack()

def notificar(titulo, mensaje):
    toaster.show_toast(
        titulo,
        mensaje,
        duration=5,
        threaded=True
    )

def ciclo_pomodoro(ciclo_comida: Optional[Callable] = None):
    notificar_mensaje = True
    for i in range(25):
        if ciclo_comida:
            ciclo_comida()

        if notificar_mensaje:
            notificar("⏰ Ciclo Pomodoro", "¡Hora de trabajar!")
            notificar_mensaje = False

        mostrar_mensaje(f"Trabajando..., vas {i} minutos")
        time.sleep(60)

def ciclo_almuerzo():
    if time.localtime().tm_hour == 13 and time.localtime().tm_min >= 0 and time.localtime().tm_min <= 30:
        mostrar_mensaje("¡Hora de almorzar!")
        notificar("🍽️ ¡Hora de almorzar!", "Tómate 30 minutos para recargar energías.")
        time.sleep(30 * 60)

def ciclo_descanso():
    notificar("⏸️ ¡Hora de descansar!", "Tómate 5 minutos de descanso.")
    for i in range(5):
        mostrar_mensaje(f"¡Hora de descansar!, vas {i} minutos")
        time.sleep(60)

def mostrar_mensaje(mensaje: str):
    # os.system('cls' if os.name == 'nt' else 'clear')
    # print(mensaje)

    label_mensaje.config(text=mensaje)
    root.update()

    __dirname = os.path.dirname(__file__)
    if not os.path.exists(f'{__dirname}/logs'):
        os.makedirs(f'{__dirname}/logs')

    if not os.path.exists(f'{__dirname}/logs/ciclo-pomodoro.log'):
        with open(f'{__dirname}/logs/ciclo-pomodoro.log', 'w') as f:
            f.write("Fecha y hora del ciclo Pomodoro:\n")
    else:
        with open(f'{__dirname}/logs/ciclo-pomodoro.log', 'a') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {mensaje}\n")

def ciclo_cena():
    fecha_actual_datetime = datetime.now()
    inicio = fecha_actual_datetime.replace(hour=19, minute=30, second=0, microsecond=0)
    fin = inicio.replace(hour=20, minute=30, second=0, microsecond=0)
    if fecha_actual_datetime > inicio and fecha_actual_datetime < fin:
        mostrar_mensaje("¡Hora de cenar!")
        notificar("🍽️ ¡Hora de cenar!", "Tómate 60 minutos para relajarte.")
        time.sleep(60 * 60)

def run_pomodoro():
    ciclo_adicional = 'n'
    while True:
        fecha_actual = time.localtime()
        fecha_actual_datetime = datetime.now()
        inicio = fecha_actual_datetime.replace(hour=19, minute=0, second=0, microsecond=0)
        fin = (inicio + timedelta(days=1)).replace(hour=2, minute=0, second=0, microsecond=0)

        if fecha_actual.tm_hour >= 8 and fecha_actual.tm_hour < 18 :
            ciclo_pomodoro(ciclo_almuerzo)
            ciclo_descanso()
        else:
            if ciclo_adicional != 's':
                notificar("⏸️ Fuera del horario laboral", "Quieres trabajar fuera del horario laboral?, confirma con la aplicación.")
                ciclo_adicional = input("¿Deseas agregar un ciclo adicional? (s/n): ").strip().lower()

            if ciclo_adicional == 's' and fecha_actual_datetime > inicio and fecha_actual_datetime < fin:
                ciclo_pomodoro(ciclo_cena)
                ciclo_descanso()
            else:
                mostrar_mensaje("Fuera del horario laboral. Ciclo Pomodoro pausado.")
                mensaje = "Ciclo Pomodoro pausado hasta las 19." if ciclo_adicional == 's' else "Ciclo Pomodoro pausado hasta mañana."
                notificar("⏸️ Fuera del horario laboral", mensaje)

                minutos_descanso = inicio - fecha_actual_datetime
                minutos_descanso = int(minutos_descanso.total_seconds() // 60)
                while minutos_descanso > 0:
                    mostrar_mensaje(f"Esperando a reiniciar el trabajo..., te quedan {minutos_descanso} minutos de descanso")
                    minutos_descanso -= 1
                    time.sleep(60)
                time.sleep(60)

            if ciclo_adicional == 'n':
                time.sleep(5)
                break


if __name__ == "__main__":
    threading.Thread(target=run_pomodoro, daemon=True).start()
    root.mainloop()