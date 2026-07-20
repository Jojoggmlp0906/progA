import tkinter as tk
from tkinter import colorchooser

class DesenhoView(tk.Tk):
    def __init__(self, controller=None):
        super().__init__()
        self.title("Paint 2.0 - Edição Avançada")
        self.geometry("850x650")

        self.controller = controller
        self.ferramenta_atual = tk.StringVar(value="selecao")
        self.cor_borda = "black"
        self.cor_preenchimento = ""
        self.on_escolher_cor_borda = None
        self.on_escolher_cor_preenchimento = None

        self._criar_widgets()

    def _criar_widgets(self):
        barra_ferramentas = tk.Frame(self, bg="lightgray")
        barra_ferramentas.pack(side=tk.TOP, fill=tk.X, pady=5)

        tk.Radiobutton(barra_ferramentas, text="✨ Selecionar", variable=self.ferramenta_atual, value="selecao", fg="blue").pack(side=tk.LEFT, padx=5)
        tk.Label(barra_ferramentas, text="|", bg="lightgray").pack(side=tk.LEFT, padx=2)

        tk.Radiobutton(barra_ferramentas, text="Linha", variable=self.ferramenta_atual, value="linha").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Rabisco", variable=self.ferramenta_atual, value="rabisco").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Retângulo", variable=self.ferramenta_atual, value="retangulo").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Oval", variable=self.ferramenta_atual, value="oval").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Círculo", variable=self.ferramenta_atual, value="circulo").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Polígono", variable=self.ferramenta_atual, value="poligono").pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(barra_ferramentas, text="Regular", variable=self.ferramenta_atual, value="regular").pack(side=tk.LEFT, padx=3)

        tk.Button(barra_ferramentas, text="Agrupar", command=self._agrupar_figuras).pack(side=tk.LEFT, padx=5)

        tk.Button(barra_ferramentas, text="Contorno", command=self._escolher_cor_borda).pack(side=tk.LEFT, padx=3)
        tk.Button(barra_ferramentas, text="Preenchimento", command=self._escolher_cor_preenchimento).pack(side=tk.LEFT, padx=3)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _escolher_cor_borda(self):
        cor = colorchooser.askcolor(title="Escolha a cor do contorno")[1]
        if cor:
            self.cor_borda = cor
            if self.on_escolher_cor_borda: self.on_escolher_cor_borda(cor)
            return cor

    def _escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")[1]
        if cor:
            self.cor_preenchimento = cor
            if self.on_escolher_cor_preenchimento: self.on_escolher_cor_preenchimento(cor)
            return cor

    def _agrupar_figuras(self):
        if self.controller:
            self.controller._agrupar_figuras()

    def atualizar_tela(self, lista_figuras, figuras_selecionadas=None, caixa_retangular=None):
        self.canvas.delete("all")
        for figura in lista_figuras:
            figura.renderizar(self.canvas)

        if figuras_selecionadas:
            for figura in figuras_selecionadas:
                figura.renderizar_caixa_selecao(self.canvas)

        # Desenha caixa retangular temporária de seleção por área
        if caixa_retangular:
            x1, y1, x2, y2 = caixa_retangular
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", dash=(2, 2))
