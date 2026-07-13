import tkinter as tk
from tkinter import colorchooser

class DesenhoView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint2.0")
        self.geometry("800x600")

        # Estado interno da UI (Ferramenta e Cores selecionadas)
        self.ferramenta_atual = tk.StringVar(value="retangulo")
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        self._criar_widgets()

    def _criar_widgets(self):
        # Barra de ferramentas superior
        barra_ferramentas = tk.Frame(self, bg="lightgray", padding=5)
        barra_ferramentas.pack(side=tk.TOP, fill=tk.X)

        # Botões de seleção de Formas
        tk.Radiobutton(barra_ferramentas, text="Retângulo", variable=self.ferramenta_atual, value="retangulo").pack(side=tk.LEFT, px=5)
        tk.Radiobutton(barra_ferramentas, text="Oval", variable=self.ferramenta_atual, value="oval").pack(side=tk.LEFT, px=5)
        tk.Radiobutton(barra_ferramentas, text="Círculo", variable=self.ferramenta_atual, value="circulo").pack(side=tk.LEFT, px=5)

        # Botões de seleção de Cores
        tk.Button(barra_ferramentas, text="Cor Contorno", command=self._escolher_cor_borda).pack(side=tk.LEFT, px=5)
        tk.Button(barra_ferramentas, text="Cor Preenchimento", command=self._escolher_cor_preenchimento).pack(side=tk.LEFT, px=5)

        # Área de desenho (Canvas)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _escolher_cor_borda(self):
        cor = colorchooser.askcolor(title="Escolha a cor do contorno")[1]
        if cor:
            self.cor_borda = cor

    def _escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")[1]
        self.cor_preenchimento = cor if cor else "" # Permite deixar transparente

    def atualizar_tela(self, lista_figuras):
        """Limpa o canvas e renderiza todas as figuras novamente."""
        self.canvas.delete("all")
        for figura in lista_figuras:
            figura.renderizar(self.canvas)
