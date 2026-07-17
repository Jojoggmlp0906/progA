from model.figuras import DesenhoModel
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
        self.figura_selecionada = None  
        self.copia_buffer = None        
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
        
        self.view.bind("<Control-c>", self._copiar_figura)
        self.view.bind("<Control-v>", self._colar_figura)
        self.view.bind("<Control-C>", self._copiar_figura)
        self.view.bind("<Control-V>", self._colar_figura)
        
        
        self.view.bind("<Delete>", self._deletar_figura)
        self.view.bind("<BackSpace>", self._deletar_figura)
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
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

    def _ao_soltar(self, event):
        estado = self._obter_estado_atual()
        if estado:
            estado.soltar(event, self.figura_atual)
            self.figura_atual = None
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

   

    def _copiar_figura(self, event=None):
        if self.figura_selecionada:
            self.copia_buffer = self.figura_selecionada
            print("Figura copiada!")

    def _colar_figura(self, event=None):
        if self.copia_buffer:
            
            nova_figura = self.copia_buffer.clonar(desvio=30)
            self.model.adicionar_figura(nova_figura)
            
           
            self.figura_selecionada = nova_figura
            self.copia_buffer = nova_figura
            
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            print("Figura colada!")

    def _deletar_figura(self, event=None):
        
        if self.figura_selecionada:
            self.model.remover_figura(self.figura_selecionada)
            self.figura_selecionada = None 
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            print("Figura deletada!")

    def _finalizar_poligono(self, event=None):
        estado = self._obter_estado_atual()
        if estado and hasattr(estado, "finalizar"):
            if estado.finalizar():
                self.figura_atual = None
                self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

    def _trazer_para_frente(self, event=None):
        if self.figura_selecionada:
            self.model.trazer_para_frente(self.figura_selecionada)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            print("Figura movida para frente")

    def _enviar_para_tras(self, event=None):
        if self.figura_selecionada:
            self.model.enviar_para_tras(self.figura_selecionada)
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)
            print("Figura movida para trás")

    def _selecionar_cor_borda(self, cor):
        self.view.cor_borda = cor
        if self.figura_selecionada is not None:
            self.figura_selecionada.cor_borda = cor
            self.view.atualizar_tela(self.model.obter_figuras(), self.figura_selecionada)

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
