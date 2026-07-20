from abc import ABC, abstractmethod
from tkinter import simpledialog
from model.figuras import Linha, Rabisco, Retangulo, Circulo, Oval, Poligono, PoligonoRegular

class EstadoDesenho(ABC):
    @abstractmethod
    def pressionar(self, event, cor_borda, cor_preenchimento): pass
    @abstractmethod
    def arrastar(self, event, figura_atual): pass
    @abstractmethod
    def soltar(self, event, figura_atual): pass


class EstadoLinha(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Linha(event.x, event.y, event.x, event.y, cor_borda)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2, figura_atual.y2 = event.x, event.y

    def soltar(self, event, figura_atual): pass


class EstadoRabisco(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Rabisco([(event.x, event.y)], cor_borda)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.pontos.append((event.x, event.y))

    def soltar(self, event, figura_atual): pass


class EstadoRetangulo(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Retangulo(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2, figura_atual.y2 = event.x, event.y

    def soltar(self, event, figura_atual): pass


class EstadoCirculo(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Circulo(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2, figura_atual.y2 = event.x, event.y

    def soltar(self, event, figura_atual): pass


class EstadoOval(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        return Oval(event.x, event.y, event.x, event.y, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual:
            figura_atual.x2, figura_atual.y2 = event.x, event.y

    def soltar(self, event, figura_atual): pass


class EstadoPoligono(EstadoDesenho):
    def __init__(self):
        self.poligono = None

    def pressionar(self, event, cor_borda, cor_preenchimento):
        if self.poligono is None:
            self.poligono = Poligono([(event.x, event.y), (event.x, event.y)], cor_borda, cor_preenchimento)
            return self.poligono
        self.poligono.pontos[-1] = (event.x, event.y)
        self.poligono.pontos.append((event.x, event.y))
        return self.poligono

    def arrastar(self, event, figura_atual):
        if figura_atual and isinstance(figura_atual, Poligono):
            figura_atual.pontos[-1] = (event.x, event.y)

    def soltar(self, event, figura_atual): pass

    def finalizar(self):
        if self.poligono and len(self.poligono.pontos) > 2:
            self.poligono.pontos.pop()
            self.poligono = None
            return True
        return False


class EstadoPoligonoRegular(EstadoDesenho):
    def pressionar(self, event, cor_borda, cor_preenchimento):
        lados = simpledialog.askinteger("Polígono regular", "Número de lados:", parent=event.widget.master, minvalue=3, initialvalue=5)
        if not lados: lados = 5
        return PoligonoRegular(event.x, event.y, event.x, event.y, lados, cor_borda, cor_preenchimento)

    def arrastar(self, event, figura_atual):
        if figura_atual and isinstance(figura_atual, PoligonoRegular):
            figura_atual.x2, figura_atual.y2 = event.x, event.y

    def soltar(self, event, figura_atual): pass


class EstadoSelecao(EstadoDesenho):
    def __init__(self, controller):
        self.controller = controller
        self.inicio_x = 0
        self.inicio_y = 0
        self.ultimo_x = 0
        self.ultimo_y = 0
        self.modo_arraste = False # True = Movendo figuras | False = Caixa de Seleção Retangular

    def pressionar(self, event, cor_borda, cor_preenchimento):
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.ultimo_x = event.x
        self.ultimo_y = event.y

        figura = self.controller.model.buscar_figura_por_posicao(event.x, event.y)
        shift_pressionado = (event.state & 0x0001) != 0

        if figura:
            self.modo_arraste = True
            if shift_pressionado:
                if figura in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas.remove(figura)
                else:
                    self.controller.figuras_selecionadas.add(figura)
            else:
                if figura not in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas = {figura}
        else:
            self.modo_arraste = False
            if not shift_pressionado:
                self.controller.figuras_selecionadas.clear()
        return None

    def arrastar(self, event, figura_atual):
        if self.modo_arraste:
            # Mover figuras selecionadas
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y
            for f in self.controller.figuras_selecionadas:
                f.mover(dx, dy)
            self.ultimo_x = event.x
            self.ultimo_y = event.y
            self.controller.caixa_selecao_retangular = None
        else:
            # Desenhando caixa visual de seleção em área
            self.controller.caixa_selecao_retangular = (self.inicio_x, self.inicio_y, event.x, event.y)

    def soltar(self, event, figura_atual):
        if not self.modo_arraste and self.controller.caixa_selecao_retangular:
            x1, y1, x2, y2 = self.controller.caixa_selecao_retangular
            # Seleciona todas as formas completamente contidas no retângulo
            for f in self.controller.model.obter_figuras():
                if f.esta_dentro_do_retangulo(x1, y1, x2, y2):
                    self.controller.figuras_selecionadas.add(f)
            self.controller.caixa_selecao_retangular = None
