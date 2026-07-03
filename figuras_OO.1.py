from abc import ABC, abstractmethod
from dataclasses import dataclass
import tkinter as tk
from tkinter import Canvas, Frame, StringVar, ttk
# janela do programa
janela = tk.Tk()
janela.title("Desenhos e figuras")
janela.geometry("700x700")
cor_atual = "black"

# classe figura
class Figura(ABC):
    @abstractmethod
    def desenhar(self, canvas):
        pass

    @abstractmethod
    def figura_imcompleta(self):
        pass

@dataclass
class Linha(Figura):
    ini_x: int
    ini_y: int
    fim_x: int
    fim_y: int
    cor: str


    def desenhar(self, canvas):
        canvas.create_line(self.ini_x, self.ini_y, self.fim_x, self.fim_y, fill=self.cor)

    def figura_imcompleta(self):
        return (self.ini_x, self.ini_y) == (self.fim_x, self.fim_y)

@dataclass
class Rabisco(Figura):
    pontos: list
    cor: str

    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill=self.cor)

    def figura_imcompleta(self):
        return len(self.pontos) <= 1

@dataclass
class Retangulo(Figura):
    ini_x: int
    ini_y: int
    fim_x: int
    fim_y: int
    cor: str

    def desenhar(self, canvas):
        canvas.create_rectangle(self.ini_x, self.ini_y, self.fim_x, self.fim_y, outline=self.cor, fill="")

    def figura_imcompleta(self):
        return (self.ini_x, self.ini_y) == (self.fim_x, self.fim_y)

@dataclass
class Poligono(Figura):
    pontos: list
    cor: str

    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos, outline=self.cor, fill="")

    def figura_imcompleta(self):
        return len(self.pontos) < 3

@dataclass
class Circulo(Figura):
    ini_x: int
    ini_y: int
    raio: int
    cor: str

    def desenhar(self, canvas):
        canvas.create_oval(self.ini_x - self.raio, self.ini_y - self.raio,
                           self.ini_x + self.raio, self.ini_y + self.raio,
                           outline=self.cor, fill="")

    def figura_imcompleta(self):
        return self.raio == 0

@dataclass
class Oval(Figura):
    ini_x: int
    ini_y: int
    raio_x: int
    raio_y: int
    cor: str

    def desenhar(self, canvas):
        canvas.create_oval(self.ini_x - self.raio_x, self.ini_y - self.raio_y,
                           self.ini_x + self.raio_x, self.ini_y + self.raio_y,
                           outline=self.cor, fill="")

    def figura_imcompleta(self):
        return self.raio_x == 0 or self.raio_y == 0


def figura_imcompleta(figura):
    return figura.figura_imcompleta()


def mudar_cor_fig(nova_cor):
    global cor_atual
    mapa_cores = {
        "Preto": "black",
        "Vermelho": "red",
        "Azul": "blue",
        "Verde": "green",
        "Amarelo": "yellow",
        "Roxo": "purple",
    }
    cor_atual = mapa_cores.get(nova_cor, "black")
    if nova_cor != cor_atual :
        desenhar_figuras()


figuras = []
figura_nova = None


def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()

    if tipo == 'Linha':
        figura_nova = Linha(event.x, event.y, event.x, event.y, cor_atual)
    elif tipo == 'Rabisco':
        figura_nova = Rabisco([(event.x, event.y)], cor_atual)
    elif tipo == 'Circulo':
        figura_nova = Circulo(event.x, event.y, 0, cor_atual)
    elif tipo == 'Retangulo':
        figura_nova = Retangulo(event.x, event.y, event.x, event.y,cor_atual)
    elif tipo == 'Oval':
        figura_nova = Oval(event.x, event.y, 0, 0, cor_atual)


def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova is None:
        return

    if isinstance(figura_nova, Rabisco):
        figura_nova.pontos.append((event.x, event.y))
    elif isinstance(figura_nova, Linha):
        figura_nova.fim_x = event.x
        figura_nova.fim_y = event.y
    elif isinstance(figura_nova, Circulo):
        dx = event.x - figura_nova.ini_x
        dy = event.y - figura_nova.ini_y
        figura_nova.raio = int((dx * dx + dy * dy) ** 0.5)
    elif isinstance(figura_nova, Retangulo):
        figura_nova.fim_x = event.x
        figura_nova.fim_y = event.y
    elif isinstance(figura_nova, Oval):
        figura_nova.raio_x = abs(event.x - figura_nova.ini_x)
        figura_nova.raio_y = abs(event.y - figura_nova.ini_y)

    desenhar_figuras()
    figura_nova.desenhar(canvas)


def incluir_figura_nova(event):
    global figura_nova
    if figura_nova is not None and not figura_nova.figura_imcompleta():
        figuras.append(figura_nova)
    figura_nova = None
    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")
    for fig in figuras:
        fig.desenhar(canvas)
    if figura_nova is not None:
        figura_nova.desenhar(canvas)


frame = Frame(janela)
paddings = {'padx': 5, 'pady': 5}

# menu de opção de figuras, linha ou rabisco
tipo_figura_var = StringVar(janela)
tipo_figura_var.set('Linha')
option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha',
                              'Linha', 'Rabisco', 'Circulo', 'Retangulo', 'Oval')
option_menu.grid(column=0, row=0, sticky='W', **paddings)


tipo_cor_var = StringVar(janela)
tipo_cor_var.set('Preto')
option_menu_cor = ttk.OptionMenu(frame, tipo_cor_var, 'Preto',
                                 'Preto', 'Vermelho', 'Azul', 'Verde', 'Amarelo', 'Roxo', command=mudar_cor_fig)
option_menu_cor.grid(column=1, row=0, sticky='W', **paddings)

canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=4, sticky='W', **paddings)

frame.pack()

canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

janela.mainloop()
