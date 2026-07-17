from model.figuras import DesenhoModel, FormaComposta
from view import DesenhoView
from estados import EstadoLinha, EstadoRabisco, EstadoRetangulo, EstadoCirculo, EstadoOval, EstadoPoligono, EstadoPoligonoRegular, EstadoSelecao

class DesenhoController:
    def __init__(self):
        self.model = DesenhoModel()
        self.view = DesenhoView(self)
        
        self.estados = {
            "selecao": EstadoSelecao(self),
            "linha": EstadoLinha(),
            "rabisco": EstadoRabisco(),
            "retangulo": EstadoRetangulo(),
            "circulo": EstadoCirculo(),
            "oval": EstadoOval(),
            "poligono": EstadoPoligono(),
            "regular": EstadoPoligonoRegular()
        }
        
        self.figura_atual = None       
        self.figuras_selecionadas = set() 
        self.copia_buffer = []            
        self._conectar_eventos()

    def _obter_estado_atual(self):
        ferramenta = self.view.ferramenta_atual.get()
        return self.estados.get(ferramenta)

    def _conectar_eventos(self):
        self.view.canvas.bind("<ButtonPress-1>", self._ao_pressionar)
        self.view.canvas.bind("<B1-Motion>", self._ao_arrastar)
        self.view.canvas.bind("<ButtonRelease-1>", self._ao_soltar)
        self.view.canvas.bind("<ButtonPress-3>", self._finalizar_poligono)

        self.view.on_escolher_cor_borda = self._selecionar_cor_borda
        self.view.on_escolher_cor_preenchimento = self._selecionar_cor_preenchimento
        
        self.view.bind("<Control-c>", self._copiar_figuras)
        self.view.bind("<Control-v>", self._colar_figuras)
        self.view.bind("<Control-C>", self._copiar_figuras)
        self.view.bind("<Control-V>", self._colar_figuras)
        
        self.view.bind("<Delete>", self._deletar_figuras)
        self.view.bind("<BackSpace>", self._deletar_figuras)
        self.view.bind("<Control-Right>", self._trazer_para_frente)
        self.view.bind("<Control-Left>", self._enviar_para_tras)

    def _ao_pressionar(self, event):
        estado = self._obter_estado_atual()
        if estado:
            retorno = estado.pressionar(event, self.view.cor_borda, self.view.cor_preenchimento)
            
            if retorno:
                self.figura_atual = retorno
                if retorno not in self.model.obter_figuras():
                    self.model.adicionar_figura(self.figura_atual)
                self.figura_selecionada = self.figura_atual
                
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

    def _ao_arrastar(self, event):
        estado = self._obter_estado_atual()
        if estado:
            estado.arrastar(event, self.figura_atual)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _ao_soltar(self, event):
        estado = self._obter_estado_atual()
        if estado:
            estado.soltar(event, self.figura_atual)
            self.figura_atual = None
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _copiar_figuras(self, event=None):
        if self.figuras_selecionadas:
            self.copia_buffer = list(self.figuras_selecionadas)

    def _colar_figuras(self, event=None):
        if self.copia_buffer:
            novos_clones = set()
            for figura in self.copia_buffer:
                novo_clone = figura.clonar(desvio=30)
                self.model.adicionar_figura(novo_clone)
                novos_clones.add(novo_clone)
            self.figuras_selecionadas = novos_clones
            self.copia_buffer = list(novos_clones)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _deletar_figuras(self, event=None):
        if self.figuras_selecionadas:
            for figura in list(self.figuras_selecionadas):
                self.model.remover_figura(figura)
            self.figuras_selecionadas.clear()
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _finalizar_poligono(self, event=None):
        estado = self._obter_estado_atual()
        if estado and hasattr(estado, "finalizar"):
            if estado.finalizar():
                self.figura_atual = None
                self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

    def _trazer_para_frente(self, event=None):
        if self.figuras_selecionadas:
            for figura in self.figuras_selecionadas:
                self.model.trazer_para_frente(figura)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _enviar_para_tras(self, event=None):
        if self.figuras_selecionadas:
            for figura in list(self.figuras_selecionadas):
                self.model.enviar_para_tras(figura)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _agrupar_figuras(self, event=None):
        figuras = [figura for figura in self.model.obter_figuras() if not isinstance(figura, FormaComposta)]
        if len(figuras) < 2:
            return

        forma_composta = self.model.criar_forma_composta(figuras)
        if forma_composta:
            self.figura_selecionada = forma_composta
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            print("Figuras agrupadas!")

    def _selecionar_cor_borda(self, cor):
        self.view.cor_borda = cor
        for figura in self.figuras_selecionadas:
            figura.cor_borda = cor
        self.view.atualizar_tela(self.model.obter_figuras(), self.figuras_selecionadas)

    def _selecionar_cor_preenchimento(self, cor):
        self.view.cor_preenchimento = cor if cor else ""
        if self.figura_selecionada is not None and hasattr(self.figura_selecionada, "cor_preenchimento"):
            self.figura_selecionada.cor_preenchimento = cor if cor else ""
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            
    def executar(self):
        self.view.mainloop()

if __name__ == "__main__":
    app = DesenhoController()
    app.executar()
