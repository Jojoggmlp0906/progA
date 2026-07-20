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
    def __init__(self):
        self.em_construcao = False

    def pressionar(self, event, cor_borda, cor_preenchimento):
        # Se NÃO está em construção, este é o PRIMEIRO clique (define o início/centro)
        if not self.em_construcao:
            lados = simpledialog.askinteger(
                "Polígono regular", 
                "Número de lados:", 
                parent=event.widget.master, 
                minvalue=3, 
                initialvalue=5
            )
            # Se o usuário cancelar, não faz nada
            if lados is None:
                return None
            
            self.em_construcao = True
            event.widget.bind("<MouseWheel>", lambda e: self.mudar_lados_scroll(e, event.widget))
            # Cria o polígono no ponto clicado
            return PoligonoRegular(event.x, event.y, event.x, event.y, lados, cor_borda, cor_preenchimento)
        
        # Se JÁ ESTÁ em construção, este é o SEGUNDO clique (confirma e finaliza)
        else:
            self.em_construcao = False
            # Retorna None para o Controller entender que a figura foi finalizada
            event.widget.unbind("<MouseWheel>")
            return None

    def arrastar(self, event, figura_atual):
        # Usado se o usuário mover segurando o botão (comportamento legado, mantido por segurança)
        if figura_atual and isinstance(figura_atual, PoligonoRegular):
            figura_atual.x2 = event.x
            figura_atual.y2 = event.y
            
   def mudar_lados_scroll(self, event, canvas):
       "Captura o scrooll do mouse para aumentar ou diminuir os lados."
       figura_atual = canvas.master.controller.figura_atual
       if figura_atual and isinstance(figura_atual, PoligonoRegular):
          if event.delta > 0:
              figura_atual.set_lados(figura_atual.lados + 1)
          elif event.delta < 0 and figura_atual.lados > 3:
              figura_atual.set_lados(figura_atual.lados - 1)
              
    def soltar(self, event, figura_atual):
        # Não faz nada ao soltar o botão no primeiro clique
        pass

class EstadoSelecao(EstadoDesenho):
    def __init__(self, controller):
        self.controller = controller
        self.ultimo_x = 0
        self.ultimo_y = 0
        
        # Atributos para gerenciar a área do retângulo de seleção
        self.inicio_x = 0
        self.inicio_y = 0
        self.retangulo_visual_id = None
        self.modo_retangulo = False

    def pressionar(self, event, cor_borda, cor_preenchimento):
        figura = self.controller.model.buscar_figura_por_posicao(event.x, event.y)
        shift_pressionado = (event.state & 0x0001) != 0

        self.ultimo_x = event.x
        self.ultimo_y = event.y

        if figura:
            self.modo_retangulo = False
            if shift_pressionado:
                if figura in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas.remove(figura)
                else:
                    self.controller.figuras_selecionadas.add(figura)
            else:
                if figura not in self.controller.figuras_selecionadas:
                    self.controller.figuras_selecionadas = {figura}
        else:
            # Ativa a seleção por área retangular ao clicar no vazio
            self.modo_retangulo = True
            self.inicio_x = event.x
            self.inicio_y = event.y
            
            if not shift_pressionado:
                self.controller.figuras_selecionadas.clear()

        return None 

    def arrastar(self, event, figura_atual):
        if self.modo_retangulo:
            canvas = self.controller.view.canvas
            # Apaga o retângulo do frame anterior para o efeito dinâmico de arrasto
            if self.retangulo_visual_id:
                canvas.delete(self.retangulo_visual_id)
            
            # Cria a linha tracejada azul que delimita a área do retângulo
            self.retangulo_visual_id = canvas.create_rectangle(
                self.inicio_x, self.inicio_y, event.x, event.y,
                outline="#0078d7", dash=(4, 4), width=1.5
            )
        else:
            # Modo padrão: Mover objetos selecionados
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y

            for figura in self.controller.figuras_selecionadas:
                figura.mover(dx, dy)

            self.ultimo_x = event.x
            self.ultimo_y = event.y

    def soltar(self, event, figura_atual):
        if self.modo_retangulo:
            canvas = self.controller.view.canvas
            # Limpa o retângulo tracejado da tela
            if self.retangulo_visual_id:
                canvas.delete(self.retangulo_visual_id)
                self.retangulo_visual_id = None
            
            # Determina as fronteiras do retângulo de seleção (AABB)
            sel_x1 = min(self.inicio_x, event.x)
            sel_x2 = max(self.inicio_x, event.x)
            sel_y1 = min(self.inicio_y, event.y)
            sel_y2 = max(self.inicio_y, event.y)
            
            # Tolerância para evitar cliques fantasmas
            if (sel_x2 - sel_x1) > 4 or (sel_y2 - sel_y1) > 4:
                for figura in self.controller.model.obter_figuras():
                    fig_x1, fig_y1, fig_x2, fig_y2 = None, None, None, None
                    
                    # 1. Identifica os limites para figuras com propriedades x1, y1 (Linhas, Retângulos, etc)
                    if hasattr(figura, 'x1') and hasattr(figura, 'y1'):
                        fig_x1, fig_x2 = min(figura.x1, figura.x2), max(figura.x1, figura.x2)
                        fig_y1, fig_y2 = min(figura.y1, figura.y2), max(figura.y1, figura.y2)
                    
                    # 2. Identifica os limites para figuras baseadas em listas de pontos (Polígonos, Rabiscos)
                    elif hasattr(figura, 'pontos') and figura.pontos:
                        lista_x = [p[0] for p in figura.pontos]
                        lista_y = [p[1] for p in figura.pontos]
                        fig_x1, fig_x2 = min(lista_x), max(lista_x)
                        fig_y1, fig_y2 = min(lista_y), max(lista_y)
                    
                    # Teste de Interseção Retangular (Colisão AABB)
                    if fig_x1 is not None:
                        # Se as caixas se sobrepõem em ambos os eixos, há colisão/contato
                        colisao_x = (fig_x1 <= sel_x2) and (fig_x2 >= sel_x1)
                        colisao_y = (fig_y1 <= sel_y2) and (fig_y2 >= sel_y1)
                        
                        if colisao_x and colisao_y:
                            self.controller.figuras_selecionadas.add(figura)

            self.modo_retangulo = False
            # Renderiza as caixas de seleção nos objetos que estavam dentro/tocando o retângulo
            self.controller.view.atualizar_tela(
                self.controller.model.obter_figuras(), 
                self.controller.figuras_selecionadas
            )
