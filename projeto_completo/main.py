from model.figuras import DesenhoModel
from view import DesenhoView
from estados import EstadoLinha, EstadoRabisco, EstadoRetangulo, EstadoCirculo, EstadoOval

class DesenhoController:
    def __init__(self):
        self.model = DesenhoModel()
        self.view = DesenhoView()
        
        # Mapeia a string da view para a respectiva classe de Estado
        self.estados = {
            "linha": EstadoLinha(),
            "rabisco": EstadoRabisco(),
            "retangulo": EstadoRetangulo(),
            "circulo": EstadoCirculo(),
            "oval": EstadoOval()
        }
        
        self.figura_atual = None
        self._conectar_eventos()

    def _obter_estado_atual(self):
        # Pega o valor selecionado nos Radiobuttons da View
        ferramenta = self.view.ferramenta_atual.get()
        return self.estados.get(ferramenta)

    def _conectar_eventos(self):
        # Vincula os eventos de mouse do Canvas às funções do controlador
        self.view.canvas.bind("<ButtonPress-1>", self._ao_pressionar)
        self.view.canvas.bind("<B1-Motion>", self._ao_arrastar)
        self.view.canvas.bind("<ButtonRelease-1>", self._ao_soltar)

    def _ao_pressionar(self, event):
        estado = self._obter_estado_atual()
        if estado:
            # Cria a figura temporária com as cores selecionadas no momento
            self.figura_atual = estado.pressionar(event, self.view.cor_borda, self.view.cor_preenchimento)
            
            # Adiciona temporariamente ao modelo para termos feedback visual instantâneo
            self.model.adicionar_figura(self.figura_atual)
            self.view.atualizar_tela(self.model.obter_figuras())

    def _ao_arrastar(self, event):
        estado = self._obter_estado_atual()
        if estado and self.figura_atual:
            estado.arrastar(event, self.figura_atual)
            # Atualiza a tela enquanto arrasta para ver a animação do desenho crescendo
            self.view.atualizar_tela(self.model.obter_figuras())

    def _ao_soltar(self, event):
        estado = self._obter_estado_atual()
        if estado and self.figura_atual:
            estado.soltar(event, self.figura_atual)
            self.figura_atual = None  # Libera a figura atualizada
            self.view.atualizar_tela(self.model.obter_figuras())

    def executar(self):
        self.view.mainloop()

if __name__ == "__main__":
    app = DesenhoController()
    app.executar()