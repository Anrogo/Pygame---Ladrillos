import tkinter as tk
import os

color_azul = '#000040'

def newWindow():
    nuevaVentana = tk.Tk()
    nuevaVentana.geometry('640x360+600+300')
    nuevaVentana.resizable(0,0)
    nuevaVentana.configure(background=color_azul)
    cadena = "PYGAME"
    etiqueta1 = tk.Label(nuevaVentana,text=cadena, font=("Arial Bold", 26), bg=color_azul, fg="green")

    etiqueta1.pack(fill = tk.X, padx=10,pady=10, side = tk.TOP) # fill llena toda la línea

    cadena2 = "Nice game, would you like to continue playing?"

    etiqueta2 = tk.Label(nuevaVentana,text=cadena2, font=("Arial Bold", 15), bg=color_azul, fg="white")

    etiqueta2.pack(fill = tk.X, padx=10,pady=10, side = tk.TOP)

    boton = tk.Button(nuevaVentana,text="Play again", bg="black", font=("Arial", 30), fg="white", command = lambda:[nuevaVentana.destroy(), play()])
    boton.pack(padx=20,pady=20)

    boton2 = tk.Button(nuevaVentana,text="No, thanks", bg="black", font=("Arial", 30), fg="white", command = nuevaVentana.destroy)
    boton2.pack(padx=20,pady=20)

# Función que ejecuta el juego y una vez acabe, o lo cerremos, nos preguntará si queremos echar otra partida ejecutando de nuevo esta función, y por tanto, el juego
def play():

    os.system('python videojuego.py')
    newWindow()


ventana = tk.Tk()
ventana.title('Breakout')
# Ancho x Alto
ventana.geometry('640x360+600+300')
ventana.resizable(0,0)
ventana.configure(background=color_azul)
#cadena = "En este juego tendrás que rebotar la pelota contra una pared de ladrillos hasta que no quede ninguno.. Cuidado! Solo tendrás 3 vidas para conseguirlo"
cadena = "PYGAME"
etiqueta1 = tk.Label(ventana,text=cadena, font=("Arial Bold", 26), bg=color_azul, fg="green")

etiqueta1.pack(fill = tk.X, padx = 10,pady = 10, side = tk.TOP) # fill llena toda la línea

boton = tk.Button(ventana,text="Play", bg="black", font=("Arial", 30), fg="white", command = lambda:[ventana.destroy(), play()])
boton.pack(padx = 20, pady = 20)
boton.place(x = 200, y = 140)

boton2 = tk.Button(ventana,text="Quit", bg="black", font=("Arial", 30), fg="white", command = ventana.destroy)
boton2.pack(padx = 20, pady = 20)
boton2.place(x = 340, y = 140)

# Genera la ventana indefinidamente hasta que la cerremos manualmente
ventana.mainloop()