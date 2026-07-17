from abc import ABC, abstractmethod
from tkinter import simpledialog
from model.figuras import Linha, Rabisco, Retangulo, Circulo, Oval, Poligono, PoligonoRegular
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


class EstadoPoligono(EstadoDesenho):
    def __init__(self):
        self.poligono = None
        self.pontos = []

    def pressionar(self, event, cor_borda, cor_preenchimento):
        if self.poligono is None:
            self.pontos = [(event.x, event.y), (event.x, event.y)]
            self.poligono = Poligono(self.pontos, cor_borda, cor_preenchimento)
            return self.poligono

        self.pontos[-1] = (event.x, event.y)
        self.pontos.append((event.x, event.y))
        return self.poligono

    def arrastar(self, event, figura_atual):
        if figura_atual and isinstance(figura_atual, Poligono):
            figura_atual.pontos[-1] = (event.x, event.y)

    def soltar(self, event, figura_atual):
        pass

    def finalizar(self):
        if self.poligono and len(self.poligono.pontos) > 3:
            self.poligono.pontos.pop()
            self.poligono = None
            self.pontos = []
            return True
        return False


class EstadoPoligonoRegular(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        lados = simpledialog.askinteger("Polígono regular", "Número de lados:", parent=event.widget.master, minvalue=3, initialvalue=5)
        if lados is None:
            lados = []
        return PoligonoRegular(event.x, event.y, event.x, event.y, lados, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual and isinstance(figura_atual, PoligonoRegular):
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y

    def soltar(self, event, figura_atual):
        pass


class EstadoSelecao(EstadoDesenho):
    def __init__(self, controller):
        self.controller = controller
        self.ultimo_x = 0
        self.ultimo_y = 0

    def pressionar(self, event, cor_borda, cor_preenchimento):
        figura = self.controller.model.buscar_figura_por_posicao(event.x, event.y)
        shift_pressionado = (event.state & 0x0001) != 0

        if figura:
            if shift_pressionado:
                if figura in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas.remove(figura)
                else:
                    self.controller.figuras_selecionadas.add(figura)
            else:
                if figura not in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas = {figura}
        else:
            if not shift_pressionado:
                self.controller.figuras_selecionadas.clear()

        self.ultimo_x = event.x
        self.ultimo_y = event.y
        return None 

    def arrastar(self, event, figura_atual):
        dx = event.x - self.ultimo_x
        dy = event.y - self.ultimo_y

        for figura in self.controller.figuras_selecionadas:
            figura.mover(dx, dy)

        self.ultimo_x = event.x
        self.ultimo_y = event.y

    def soltar(self, event, figura_atual):
        pass
