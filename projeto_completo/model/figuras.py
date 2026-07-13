import math

class Figura:
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

class Linha(Figura):
    def renderizar(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

class Retangulo(Figura):
    def renderizar(self, canvas):
        return canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, 
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

class Oval(Figura):
    def renderizar(self, canvas):
        return canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

class Circulo(Figura):
    def renderizar(self, canvas):
        # Calcula o raio dinamicamente com base no ponto inicial e final
        raio = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        return canvas.create_oval(
            self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

class Rabisco:
    def __init__(self, pontos, cor_borda="black"):
        self.pontos = pontos  # Lista de tuplas [(x1, y1), (x2, y2), ...]
        self.cor_borda = cor_borda

    def renderizar(self, canvas):
        if len(self.pontos) > 1:
            # Converte a lista de tuplas em uma lista plana [x1, y1, x2, y2, ...]
            pontos_planos = [coord for pt in self.pontos for coord in pt]
            return canvas.create_line(pontos_planos, fill=self.cor_borda, smooth=True)

class DesenhoModel:
    def __init__(self):
        self.figuras = []

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def obter_figuras(self):
        return self.figuras