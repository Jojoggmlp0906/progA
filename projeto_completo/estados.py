from abc import ABC, abstractmethod
from model.figuras import Linha, Rabisco, Retangulo, Circulo, Oval

class EstadoDesenho(ABC):
    @abstractmethod
    def pressionar(self, event, cor_borda, cor_preenchimento):
        pass

    @abstractmethod
    def arrastar(self, event, figura_atual):
        pass

    @abstractmethod
    def soltar(self, event, figura_atual):
        pass


class EstadoLinha(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Linha(event.x, event.y, event.x, event.y, cor_borda)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y

    def soltar(self, event, figura_atual):
        pass


class EstadoRabisco(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Rabisco([(event.x, event.y)], cor_borda)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.pontos.append((event.x, event.y))

    def soltar(self, event, figura_atual):
        pass
        

class EstadoRetangulo(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Retangulo(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y

    def soltar(self, event, figura_atual):
        pass


class EstadoCirculo(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Circulo(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y

    def soltar(self, event, figura_atual):
        pass


class EstadoOval(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Oval(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y

    def soltar(self, event, figura_atual):
        pass