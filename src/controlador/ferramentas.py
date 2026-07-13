from abc import ABC, abstractmethod
from dataclasses import dataclass
from model.figuras import Linha,Rabisco,Retangulo,Circulo,Oval

class EstadoDesenho(ABC):
    @abstractmethod
    def pressionar(self, event):
        pass

    @abstractmethod
    def arrastar(self, event):
        pass

    @abstractmethod
    def soltar(self, event):
        pass


class EstadoLinha(EstadoDesenho):
    def pressionar(self, event):
        global figura_nova
        figura_nova = Linha(event.x, event.y, event.x, event.y)

    def arrastar(self, event):
        if figura_nova:
            figura_nova.fim_x = event.x
            figura_nova.fim_y = event.y

    def soltar(self, event):
       pass


class EstadoRabisco(EstadoDesenho):
    def pressionar(self, event):
        global figura_nova
        figura_nova = Rabisco([(event.x, event.y)])

    def arrastar(self, event):
        if figura_nova:
            figura_nova.pontos.append((event.x, event.y))

    def soltar(self, event):
        pass
        

class EstadoRetangulo(EstadoDesenho):
    def pressionar(self, event):
        global figura_nova
        figura_nova = Retangulo(event.x, event.y, event.x, event.y)

    def arrastar(self, event):
        if figura_nova:
            figura_nova.fim_x = event.x
            figura_nova.fim_y = event.y

    def soltar(self, event):
        pass


class EstadoCirculo(EstadoDesenho):
    def pressionar(self, event):
        global figura_nova
        figura_nova = Circulo(event.x, event.y, 0)

    def arrastar(self, event):
        if figura_nova:
            dx = event.x - figura_nova.ini_x
            dy = event.y - figura_nova.ini_y
            figura_nova.raio = int((dx * dx + dy * dy) ** 0.5)

    def soltar(self, event):
        pass


class EstadoOval(EstadoDesenho):
    def pressionar(self, event):
        global figura_nova
        figura_nova = Oval(event.x, event.y, 0, 0)

    def arrastar(self, event):
        if figura_nova:
            figura_nova.raio_x = abs(event.x - figura_nova.ini_x)
            figura_nova.raio_y = abs(event.y - figura_nova.ini_y)

    def soltar(self, event):
        pass
