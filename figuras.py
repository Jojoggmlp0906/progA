from abc import ABC,abstractmethod
from dataclasses import dataclass
from tkinter as tk

janela = tk.Tk()

class Figura[ABC]:
    @abstractmethod
    def desenhar(self,canvas):
        pass
    @abstractmethod
    def figura_imcompleta(self,canvas):
        pass


 @dataclass   
class Linha(Figura):
    ini_x : int 
    ini_y : int
    fim_x : int
    fim_y : int

    def desenhar(self,canvas):
        canvas.create_line(ini_x, ini_y, fim_x, fim_y)
        
    def figura_imcompleta(self,canvas):
        return (ini_x, ini_y) == (fim_x,fim_y)
@dataclass
class Rabisco(Figura):
    pontos1 : list

    def desenhar(self,canvas):
        canvas.create_line(pontos1)
    
    def figura_imcompleta(self,canvas):


@dataclass
class Retangulo(Figura):
     ini_x : int
     ini_y : int
     fim_x : int
     fim_y : int

     def desenhar(self,canvas):
        canvas.create_rectangle(ini_x, ini_y, fim_x, fim_y)


@dataclass
class Poligono(Figura):
     pontos2 : list

     def desenhar(self,canvas):
         canvas.create_polygon(pontos2)

@dataclass
class Circulo(Figura):
     ini_x : int
     ini_y : int
     raio : int

     def desenhar(self,canvas):
        canvas.create_oval(self.ini_x - self.raio, self.ini_y - self.raio,
                           self.ini_x + self.raio, self.ini_y + self.raio )

@dataclass
class Oval(figura):
    ini_x : int
    ini_y : int
    raio : int

    def desenhar(self,canvas):
        canvas.create_arc(self.ini_x - self.raio, self.ini_y - self.raio, 
                         self.ini_x + self.raio, self.ini_y + self.raio)





def figura_imcompleta(Figura):
    fig, ini_x, ini_y, fim_x, fim_y = figura
    if fig == 'Linha':
       C
    if fig == 'Rabisco':
       return 
    if fig == 'Retangulo':
       return
    if fig == 'circulo':
       return


def mudar_cor_fig(Figura):
    









frame =Frame(janela)

paddings = {'padx': 5,'pady': 5}


#option menu 
