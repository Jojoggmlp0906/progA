import math

class Figura:
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def clonar(self, desvio=20):
        return self.__class__(self.x1 + desvio, self.y1 + desvio, self.x2 + desvio, self.y2 + desvio, self.cor_borda, self.cor_preenchimento)

    def mover(self, dx, dy):
        
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def obter_limites(self):
       
        return min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2)

    def contem_ponto(self, px, py):
        
        x1, y1, x2, y2 = self.obter_limites()
        
        return (x1 - 4 <= px <= x2 + 4) and (y1 - 4 <= py <= y2 + 4)

    def renderizar_caixa_selecao(self, canvas):
        
        x1, y1, x2, y2 = self.obter_limites()
        canvas.create_rectangle(x1 - 4, y1 - 4, x2 + 4, y2 + 4, outline="blue", dash=(4, 4), width=1)


class Linha(Figura):
    def renderizar(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, width=2)
    
    def contem_ponto(self, px, py):
        L2 = (self.x2 - self.x1)**2 + (self.y2 - self.y1)**2
        if L2 == 0: return math.hypot(px - self.x1, py - self.y1) < 5
        t = max(0, min(1, ((px - self.x1)*(self.x2 - self.x1) + (py - self.y1)*(self.y2 - self.y1)) / L2))
        proj_x = self.x1 + t * (self.x2 - self.x1)
        proj_y = self.y1 + t * (self.y2 - self.y1)
        return math.hypot(px - proj_x, py - proj_y) < 6


class Retangulo(Figura):
    def renderizar(self, canvas):
        return canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)


class Oval(Figura):
    def renderizar(self, canvas):
        return canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)


class Circulo(Figura):
    def renderizar(self, canvas):
        raio = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        return canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, outline=self.cor_borda, fill=self.cor_preenchimento)
    
    def obter_limites(self):
        raio = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        return self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio


class Rabisco:
    def __init__(self, pontos, cor_borda="black"):
        self.pontos = pontos
        self.cor_borda = cor_borda

    def renderizar(self, canvas):
        if len(self.pontos) > 1:
            pontos_planos = [coord for pt in self.pontos for coord in pt]
            return canvas.create_line(pontos_planos, fill=self.cor_borda, smooth=True, width=2)

    def clonar(self, desvio=20):
        novos_pontos = [(x + desvio, y + desvio) for (x, y) in self.pontos]
        return Rabisco(novos_pontos, self.cor_borda)

    def mover(self, dx, dy):
        self.pontos = [(x + dx, y + dy) for (x, y) in self.pontos]

    def obter_limites(self):
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    def contem_ponto(self, px, py):
        
        for x, y in self.pontos:
            if math.hypot(px - x, py - y) < 8:
                return True
        return False

    def renderizar_caixa_selecao(self, canvas):
        x1, y1, x2, y2 = self.obter_limites()
        canvas.create_rectangle(x1 - 4, y1 - 4, x2 + 4, y2 + 4, outline="blue", dash=(4, 4), width=1)


class FormaComposta(Figura):
    def __init__(self, figuras, cor_borda="black", cor_preenchimento=""):
        self.figuras = list(figuras)
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def renderizar(self, canvas):
        for figura in self.figuras:
            figura.renderizar(canvas)

    def clonar(self, desvio=20):
        figuras_clonadas = [figura.clonar(desvio) for figura in self.figuras]
        return FormaComposta(figuras_clonadas, self.cor_borda, self.cor_preenchimento)

    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)

    def obter_limites(self):
        if not self.figuras:
            return (0, 0, 0, 0)

        limites = [figura.obter_limites() for figura in self.figuras]
        x1s = [limite[0] for limite in limites]
        y1s = [limite[1] for limite in limites]
        x2s = [limite[2] for limite in limites]
        y2s = [limite[3] for limite in limites]
        return min(x1s), min(y1s), max(x2s), max(y2s)

    def contem_ponto(self, px, py):
        return any(figura.contem_ponto(px, py) for figura in self.figuras)

    def renderizar_caixa_selecao(self, canvas):
        x1, y1, x2, y2 = self.obter_limites()
        canvas.create_rectangle(x1 - 4, y1 - 4, x2 + 4, y2 + 4, outline="blue", dash=(4, 4), width=1)


class DesenhoModel:
    def __init__(self):
        self.figuras = []

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def remover_figura(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)

    def obter_figuras(self):
        return self.figuras

    def criar_forma_composta(self, figuras):
        figuras_validas = [figura for figura in figuras if figura in self.figuras]
        if not figuras_validas:
            return None

        for figura in figuras_validas:
            self.remover_figura(figura)

        forma_composta = FormaComposta(figuras_validas)
        self.adicionar_figura(forma_composta)
        return forma_composta

    def buscar_figura_por_posicao(self, x, y):
        
        for figura in reversed(self.figuras):
            if figura.contem_ponto(x, y):
                return figura
        return None
