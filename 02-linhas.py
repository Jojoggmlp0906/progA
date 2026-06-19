from tkinter import *
import tkinter as tk
from tkinte import ttk

janela = tk.Tk()

texto=tk.Label(janela, text=" figuras e desenhos")
texto.pack()
root.geometry("300x250")

# Quando o mouse é pressionado
def inicia_linha(event):
    global ini_x, ini_y
    ini_x = event.x
    ini_y = event.y

# Quando o mouse é movido com o botão pressionado
def atualiza_linha(event):
    global fim_x, fim_y,raio
    fim_x = event.x
    fim_y = event.y
    desenhar()
    raio=()
    canvas.create_oval(ini_x-raio, ini_y-raio, ini_x+raio, ini_y+raio)
    canvas.create_line(ini_x, ini_y, fim_x, fim_y)


# Quando o mouse é solto
def incluir_linha(event):
    linhas.append((ini_x, ini_y, fim_x, fim_y))
# retangulo
def incluir_retangulo(event):
    retangulo.append(())
# circulo 
def incluir_circulo(event):
    circulo.append(())

# criação de linha
def desenhar():
    canvas.delete("all")
    for linha in linhas:
        canvas.create_line(linha[0], linha[1], linha[2], linha[3])

def desenhar():
    canvas.delete("all")
    for retangul in retangulo:
        canvas.creative.rectangle()


#******* MAIN *******#

# Todas as linhas desenhadas são armazenadas aqui
retangulo = []
circulo = []
linhas = []

root = Tk()

canvas = Canvas(root, bg='white', width=600, height=600)
canvas.pack()

ini_x = None
ini_y = None
fim_x = None
fim_y = None
canvas.bind('<ButtonPress-1>', inicia_linha)
canvas.bind('<B1-Motion>', atualiza_linha)
canvas.bind('<ButtonRelease-1>', incluir_linha)

root.mainloop()
