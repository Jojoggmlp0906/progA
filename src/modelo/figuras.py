from abc import ABC, abstractmethod
from dataclasses import dataclass

class Figura(ABC):
    @abstractmethod
    def desenhar(self, canvas, cor="black"):
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

    def desenhar(self, canvas, cor="black"):
        canvas.create_line(self.ini_x, self.ini_y, self.fim_x, self.fim_y, fill=cor)

    def figura_imcompleta(self):
        return (self.ini_x, self.ini_y) == (self.fim_x, self.fim_y)

@dataclass
class Rabisco(Figura):
    pontos: list

    def desenhar(self, canvas, cor="black"):
        canvas.create_line(self.pontos, fill=cor)

    def figura_imcompleta(self):
        return len(self.pontos) <= 1

@dataclass
class Retangulo(Figura):
    ini_x: int
    ini_y: int
    fim_x: int
    fim_y: int

    def desenhar(self, canvas, cor="black"):
        canvas.create_rectangle(self.ini_x, self.ini_y, self.fim_x, self.fim_y, outline=cor, fill="")

    def figura_imcompleta(self):
        return (self.ini_x, self.ini_y) == (self.fim_x, self.fim_y)

@dataclass
class Poligono(Figura):
    pontos: list

    def desenhar(self, canvas, cor="black"):
        canvas.create_polygon(self.pontos, outline=cor, fill="")

    def figura_imcompleta(self):
        return len(self.pontos) < 3

@dataclass
class Circulo(Figura):
    ini_x: int
    ini_y: int
    raio: int

    def desenhar(self, canvas, cor="black"):
        canvas.create_oval(self.ini_x - self.raio, self.ini_y - self.raio,
                           self.ini_x + self.raio, self.ini_y + self.raio,
                           outline=cor, fill="")

    def figura_imcompleta(self):
        return self.raio == 0

@dataclass
class Oval(Figura):
    ini_x: int
    ini_y: int
    raio_x: int
    raio_y: int

    def desenhar(self, canvas, cor="black"):
        canvas.create_oval(self.ini_x - self.raio_x, self.ini_y - self.raio_y,
                           self.ini_x + self.raio_x, self.ini_y + self.raio_y,
                           outline=cor, fill="")

    def figura_imcompleta(self):
        return self.raio_x == 0 or self.raio_y == 0


