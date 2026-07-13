import math

class Figura:
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

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
    def __init__(self, x1, y1, x2, y2, cor_borda="black", cor_preenchimento=""):
        # Ajusta os pontos para garantir que o raio seja simétrico (um círculo perfeito)
        raio = math.hypot(x2 - x1, y2 - y1)
        super().__init__(x1 - raio, y1 - raio, x1 + raio, y1 + raio, cor_borda, cor_preenchimento)

    def renderizar(self, canvas):
        return canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

class DesenhoModel:
    """Guarda a lista de todas as figuras criadas no projeto."""
    def __init__(self):
        self.figuras = []

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def obter_figuras(self):
        return self.figuras
