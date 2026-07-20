from abc import ABC, abstractmethod
import math


class Forma(ABC):
    @abstractmethod
    def renderizar(self, canvas):
        pass

    @abstractmethod
    def renderizar_caixa_selecao(self, canvas):
        pass

    @abstractmethod
    def contem_ponto(self, x, y):
        pass

    @abstractmethod
    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def mover(self, dx, dy):
        pass

    @abstractmethod
    def clonar(self, desvio=0):
        pass


class Retangulo(Forma):
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def renderizar(self, canvas):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def renderizar_caixa_selecao(self, canvas):
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        canvas.create_rectangle(min_x-2, min_y-2, max_x+2, max_y+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        return min(self.x1, self.x2) <= x <= max(self.x1, self.x2) and min(self.y1, self.y2) <= y <= max(self.y1, self.y2)

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return rx1 <= min(self.x1, self.x2) and max(self.x1, self.x2) <= rx2 and ry1 <= min(self.y1, self.y2) and max(self.y1, self.y2) <= ry2

    def mover(self, dx, dy):
        self.x1 += dx; self.y1 += dy
        self.x2 += dx; self.y2 += dy

    def clonar(self, desvio=0):
        return Retangulo(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.cor_borda, self.cor_preenchimento)


class Linha(Forma):
    def __init__(self, x1, y1, x2, y2, cor_borda="black"):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.cor_borda = cor_borda

    def renderizar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, width=2)

    def renderizar_caixa_selecao(self, canvas):
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        canvas.create_rectangle(min_x-2, min_y-2, max_x+2, max_y+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        # Distância ponto a segmento simples
        l2 = (self.x2 - self.x1)**2 + (self.y2 - self.y1)**2
        if l2 == 0: return math.hypot(x - self.x1, y - self.y1) < 5
        t = max(0, min(1, ((x - self.x1) * (self.x2 - self.x1) + (y - self.y1) * (self.y2 - self.y1)) / l2))
        proj_x = self.x1 + t * (self.x2 - self.x1)
        proj_y = self.y1 + t * (self.y2 - self.y1)
        return math.hypot(x - proj_x, y - proj_y) <= 5

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return rx1 <= min(self.x1, self.x2) and max(self.x1, self.x2) <= rx2 and ry1 <= min(self.y1, self.y2) and max(self.y1, self.y2) <= ry2

    def mover(self, dx, dy):
        self.x1 += dx; self.y1 += dy
        self.x2 += dx; self.y2 += dy

    def clonar(self, desvio=0):
        return Linha(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.cor_borda)


class Rabisco(Forma):
    def __init__(self, pontos=None, cor_borda="black"):
        self.pontos = pontos if pontos else []
        self.cor_borda = cor_borda

    def renderizar(self, canvas):
        if len(self.pontos) > 1:
            for i in range(len(self.pontos) - 1):
                canvas.create_line(self.pontos[i][0], self.pontos[i][1], self.pontos[i+1][0], self.pontos[i+1][1], fill=self.cor_borda, width=2)

    def renderizar_caixa_selecao(self, canvas):
        if not self.pontos: return
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        canvas.create_rectangle(min(xs)-2, min(ys)-2, max(xs)+2, max(ys)+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        return any(math.hypot(px - x, py - y) <= 5 for px, py in self.pontos)

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        if not self.pontos: return False
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return all(rx1 <= px <= rx2 and ry1 <= py <= ry2 for px, py in self.pontos)

    def mover(self, dx, dy):
        self.pontos = [(px + dx, py + dy) for px, py in self.pontos]

    def clonar(self, desvio=0):
        novos_pontos = [(px + desvio, py + desvio) for px, py in self.pontos]
        return Rabisco(novos_pontos, self.cor_borda)


class Oval(Forma):
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def renderizar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)

    def renderizar_caixa_selecao(self, canvas):
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        canvas.create_rectangle(min_x-2, min_y-2, max_x+2, max_y+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        rx = abs(self.x2 - self.x1) / 2
        ry = abs(self.y2 - self.y1) / 2
        if rx == 0 or ry == 0: return False
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        return (((x - cx)**2) / (rx**2)) + (((y - cy)**2) / (ry**2)) <= 1

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return rx1 <= min(self.x1, self.x2) and max(self.x1, self.x2) <= rx2 and ry1 <= min(self.y1, self.y2) and max(self.y1, self.y2) <= ry2

    def mover(self, dx, dy):
        self.x1 += dx; self.y1 += dy
        self.x2 += dx; self.y2 += dy

    def clonar(self, desvio=0):
        return Oval(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.cor_borda, self.cor_preenchimento)


class Circulo(Oval):
    def renderizar(self, canvas):
        r = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        canvas.create_oval(self.x1 - r, self.y1 - r, self.x1 + r, self.y1 + r, outline=self.cor_borda, fill=self.cor_preenchimento)

    def renderizar_caixa_selecao(self, canvas):
        r = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        canvas.create_rectangle(self.x1 - r - 2, self.y1 - r - 2, self.x1 + r + 2, self.y1 + r + 2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        r = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        return math.hypot(x - self.x1, y - self.y1) <= r

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        r = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return rx1 <= (self.x1 - r) and (self.x1 + r) <= rx2 and ry1 <= (self.y1 - r) and (self.y1 + r) <= ry2

    def clonar(self, desvio=0):
        return Circulo(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.cor_borda, self.cor_preenchimento)


class Poligono(Forma):
    def __init__(self, pontos=None, cor_borda="black", cor_preenchimento=""):
        self.pontos = pontos if pontos else []
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def renderizar(self, canvas):
        if len(self.pontos) >= 2:
            pts = [c for p in self.pontos for c in p]
            canvas.create_polygon(pts, outline=self.cor_borda, fill=self.cor_preenchimento if self.cor_preenchimento else "", width=1)

    def renderizar_caixa_selecao(self, canvas):
        if not self.pontos: return
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        canvas.create_rectangle(min(xs)-2, min(ys)-2, max(xs)+2, max(ys)+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        n = len(self.pontos)
        inside = False
        p1x, p1y = self.pontos[0]
        for i in range(n + 1):
            p2x, p2y = self.pontos[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        if not self.pontos: return False
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return all(rx1 <= px <= rx2 and ry1 <= py <= ry2 for px, py in self.pontos)

    def mover(self, dx, dy):
        self.pontos = [(px + dx, py + dy) for px, py in self.pontos]

    def clonar(self, desvio=0):
        novos_pontos = [(px + desvio, py + desvio) for px, py in self.pontos]
        return Poligono(novos_pontos, self.cor_borda, self.cor_preenchimento)


class PoligonoRegular(Forma):
    def __init__(self, x1, y1, x2, y2, lados=5, cor_borda="black", cor_preenchimento=""):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.lados = lados if isinstance(lados, int) and lados >= 3 else 5
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def _obter_pontos(self):
        r = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        angulo_passo = (2 * math.pi) / self.lados
        pontos = []
        for i in range(self.lados):
            px = self.x1 + r * math.cos(i * angulo_passo - math.pi / 2)
            py = self.y1 + r * math.sin(i * angulo_passo - math.pi / 2)
            pontos.append((px, py))
        return pontos

    def renderizar(self, canvas):
        pontos = self._obter_pontos()
        pts = [c for p in pontos for c in p]
        canvas.create_polygon(pts, outline=self.cor_borda, fill=self.cor_preenchimento if self.cor_preenchimento else "", width=1)

    def renderizar_caixa_selecao(self, canvas):
        pontos = self._obter_pontos()
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        canvas.create_rectangle(min(xs)-2, min(ys)-2, max(xs)+2, max(ys)+2, outline="blue", dash=(4, 4))

    def contem_ponto(self, x, y):
        pontos = self._obter_pontos()
        poly = Poligono(pontos)
        return poly.contem_ponto(x, y)

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        pontos = self._obter_pontos()
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        return all(rx1 <= px <= rx2 and ry1 <= py <= ry2 for px, py in pontos)

    def mover(self, dx, dy):
        self.x1 += dx; self.y1 += dy
        self.x2 += dx; self.y2 += dy

    def clonar(self, desvio=0):
        return PoligonoRegular(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.lados, self.cor_borda, self.cor_preenchimento)


class FormaComposta(Forma):
    """Padrão Composite: Agrupa múltiplas formas como se fossem uma única figura."""
    def __init__(self, formas=None):
        self.formas = formas if formas else []

    def renderizar(self, canvas):
        for forma in self.formas:
            forma.renderizar(canvas)

    def renderizar_caixa_selecao(self, canvas):
        for forma in self.formas:
            forma.renderizar_caixa_selecao(canvas)

    def contem_ponto(self, x, y):
        return any(f.contem_ponto(x, y) for f in self.formas)

    def esta_dentro_do_retangulo(self, x1, y1, x2, y2):
        return all(f.esta_dentro_do_retangulo(x1, y1, x2, y2) for f in self.formas)

    def mover(self, dx, dy):
        for forma in self.formas:
            forma.mover(dx, dy)

    def aplicar_cor_borda(self, cor):
        for f in self.formas:
            if hasattr(f, 'aplicar_cor_borda'): f.aplicar_cor_borda(cor)
            else: f.cor_borda = cor

    def aplicar_cor_preenchimento(self, cor):
        for f in self.formas:
            if hasattr(f, 'aplicar_cor_preenchimento'): f.aplicar_cor_preenchimento(cor)
            else: f.cor_preenchimento = cor

    def clonar(self, desvio=0):
        novas_formas = [f.clonar(desvio) for f in self.formas]
        return FormaComposta(novas_formas)


class DesenhoModel:
    def __init__(self):
        self._figuras = []

    def adicionar_figura(self, figura):
        self._figuras.append(figura)

    def remover_figura(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)

    def obter_figuras(self):
        return self._figuras

    def buscar_figura_por_posicao(self, x, y):
        # Percorre do topo para a base (último desenhado tem prioridade de clique)
        for figura in reversed(self._figuras):
            if figura.contem_ponto(x, y):
                return figura
        return None

    def criar_forma_composta(self, lista_figuras):
        for f in lista_figuras:
            self.remover_figura(f)
        composta = FormaComposta(lista_figuras)
        self.adicionar_figura(composta)
        return composta

    def trazer_um_passo_para_frente(self, figuras_selecionadas):
        """Move o bloco de figuras selecionadas 1 nível para frente sem alterar a ordem entre elas."""
        n = len(self._figuras)
        # Processa do topo para a base para não encavalar trocas
        for i in range(n - 2, -1, -1):
            if self._figuras[i] in figuras_selecionadas and self._figuras[i+1] not in figuras_selecionadas:
                self._figuras[i], self._figuras[i+1] = self._figuras[i+1], self._figuras[i]

    def enviar_um_passo_para_tras(self, figuras_selecionadas):
        """Move o bloco de figuras selecionadas 1 nível para trás sem alterar a ordem entre elas."""
        n = len(self._figuras)
        # Processa da base para o topo
        for i in range(1, n):
            if self._figuras[i] in figuras_selecionadas and self._figuras[i-1] not in figuras_selecionadas:
                self._figuras[i], self._figuras[i-1] = self._figuras[i-1], self._figuras[i]

    def trazer_para_frente(self, figuras_selecionadas):
        nao_selecionadas = [f for f in self._figuras if f not in figuras_selecionadas]
        selecionadas = [f for f in self._figuras if f in figuras_selecionadas]
        self._figuras = nao_selecionadas + selecionadas

    def enviar_para_tras(self, figuras_selecionadas):
        nao_selecionadas = [f for f in self._figuras if f not in figuras_selecionadas]
        selecionadas = [f for f in self._figuras if f in figuras_selecionadas]
        self._figuras = selecionadas + nao_selecionadas
