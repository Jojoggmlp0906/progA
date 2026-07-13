import tkinter as tk
from tkinter import colorchooser

class DesenhoView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint 2.0")
        self.geometry("800x600")

        self.ferramenta_atual = tk.StringVar(value="retangulo")
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        self._criar_widgets()

    def _criar_widgets(self):
        # Usando padx e pady no pack do frame em vez de padding interno direto
        barra_ferramentas = tk.Frame(self, bg="lightgray")
        barra_ferramentas.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Botões de seleção de Formas (Mudado px para padx)
        tk.Radiobutton(barra_ferramentas, text="Linha", variable=self.ferramenta_atual, value="linha").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(barra_ferramentas, text="Rabisco", variable=self.ferramenta_atual, value="rabisco").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(barra_ferramentas, text="Retângulo", variable=self.ferramenta_atual, value="retangulo").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(barra_ferramentas, text="Oval", variable=self.ferramenta_atual, value="oval").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(barra_ferramentas, text="Círculo", variable=self.ferramenta_atual, value="circulo").pack(side=tk.LEFT, padx=5)

        # Botões de seleção de Cores (Mudado px para padx)
        tk.Button(barra_ferramentas, text="Cor Contorno", command=self._escolher_cor_borda).pack(side=tk.LEFT, padx=5)
        tk.Button(barra_ferramentas, text="Cor Preenchimento", command=self._escolher_cor_preenchimento).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _escolher_cor_borda(self):
        cor = colorchooser.askcolor(title="Escolha a cor do contorno")[1]
        if cor:
            self.cor_borda = cor

    def _escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")[1]
        self.cor_preenchimento = cor if cor else ""

    def atualizar_tela(self, lista_figuras):
        self.canvas.delete("all")
        for figura in lista_figuras:
            figura.renderizar(self.canvas)