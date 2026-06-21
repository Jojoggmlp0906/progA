from tkinter import *
from tkinter import ttk
import tkinter as tk
janela = tk.Tk()

texto =tk.Label(janela, text="desenhos e figuras")
janela.title("Aplicação de figuras")
texto.pack()

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova, raio
    raio = 0 # o raio começa em 0, e vai aumentando conforme o mouse é movido
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)])
    elif tipo_figura_var.get() == 'Circulo':
        figura_nova = ("circulo", (event.x, event.y, raio)) # o terceiro valor é o raio, que começa em 0
    elif tipo_figura_var.get() == 'retangulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y)) # o terceiro e quarto valores são as coordenadas do canto inferior direito do retângulo, que começam iguais às do canto superior esquerdo
    elif tipo_figura_var.get() == 'oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y)) # o terceiro e quarto valores são as coordenadas do canto inferior direito do oval, que começam iguais às do canto superior esquerdo

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova, raio
    x_ini, y_ini = figura_nova[1][0], figura_nova[1][1] # coordenadas do ponto inicial da figura, que é o mesmo para linha, círculo, retângulo e oval
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "linha":
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "circulo":
        raio = ((event.x - x_ini)**2 + (event.y - y_ini)**2)**0.5
        figura_nova = ("circulo", (x_ini, y_ini, raio))
    elif figura_nova[0] == "retangulo":
        figura_nova = ("retangulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
        circulo.append(figura_nova)
        retangulo.append(figura_nova)
        oval.append(figura_nova)
    desenhar_figuras()

def desenhar_figuras():
    global x_inicial, y_inicial, raio
    x_inicial = figura_nova[1][0] # coordenada x do ponto inicial da figura, que é o mesmo para linha, círculo, retângulo e oval
    y_inicial = figura_nova[1][1] # coordenada y do ponto
    raio = figura_nova[1][2] # raio do círculo
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], tags="figura1")
        elif fig == "circulo":
            canvas.create_oval(values[0] - values[2], values[1] - values[2], values[0] + values[2], values[1] + values[2], tags="figura1")
        elif fig == "rabisco":
            canvas.create_line(values)
        elif fig == "retangulo":
             canvas.create_rectangle(values[0], values[1], values[2], values[3], tags="figura1")
        elif fig == "oval":
             canvas.create_oval(values[0], values[1], values[2], values[3], tags="figura1")

def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "circulo":
        canvas.create_oval(values[0] - values[2], values[1] - values[2], values[0] + values[2], values[1] + values[2], dash=(4, 2))
    elif fig == "rabisco": # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2))

def incompleta(figura):
    fig, values = figura
    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "circulo":
        return values[2] == 0
    elif fig == "rabisco":
        return len(values) <= 1


 # escolhar da cor de preenchimento       
def mudar_cor_fig(nova_cor):
        
        canvas.itemconfig("figura1",fill=nova_cor)


# escolhar da cor da borda
def mudar_cor_fig2(nova_cor2):
        
        canvas.itemconfig("figura1", outline=nova_cor2)
        
#******* MAIN *******#

oval = []         # desenho oval
retangulo = []    # desenho retangulo
circulo = []      # desenho circular
figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
raio = None       # Variável global para armazenar o raio do círculo que está sendo desenhado, para que ele possa ser atualizado conforme o mouse é movido
cores = ['Blue', 'Red', 'Green', 'Yellow', 'Purple'] # lista de opção de cores


frame = Frame(janela)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label


# option menu
tipo_figura_var = StringVar(janela) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,'Linha',
                             'Linha', 'Rabisco', 'Circulo' , 'Retangulo' , 'Oval')
option_menu.grid(column=2, row=0, sticky=W, **paddings)


 
tipo_cor_var = StringVar(janela) # Guarda a cor selecionada no option menu
option_menu = ttk.OptionMenu(frame, tipo_cor_var,'selecionar cor de preenchimento',
                             'Blue', 'Red', 'Green', 'Yellow', 'Purple', command=mudar_cor_fig)
option_menu.grid(column=2, row=0, sticky=W, **paddings)

tipo_cor_var1 = StringVar(janela)
option_menu2 = ttk.OptionMenu(frame, tipo_cor_var1,'selecionar cor da borda',
                              'Blue','Red','Green','Yellow','Purple', command=mudar_cor_fig2)
option_menu.grid(column=4,row=0,sticky=W,**paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=30, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

janela.mainloop()
