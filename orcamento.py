import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date
import sqlite3

# Banco de dados
def criar_banco():
    conn = sqlite3.connect("orcamentos.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        total REAL,
        data TEXT
    )""")
    conn.commit()
    conn.close()

def salvar_orcamento(cliente, total):
    conn = sqlite3.connect("orcamentos.db")
    c = conn.cursor()
    c.execute("INSERT INTO orcamentos (cliente, total, data) VALUES (?, ?, ?)",
              (cliente, total, date.today().strftime('%d/%m/%Y')))
    conn.commit()
    conn.close()

# Gerar PDF
def gerar_pdf(cliente, produtos):
    nome_arquivo = f"orcamento_{cliente.replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, altura - 50, "ORÇAMENTO")

    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 80, f"Cliente: {cliente}")
    c.drawString(50, altura - 100, f"Data: {date.today().strftime('%d/%m/%Y')}")
    c.drawString(50, altura - 120, f"Validade: 7 dias")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, altura - 160, "Produto")
    c.drawString(300, altura - 160, "Qtd")
    c.drawString(380, altura - 160, "Valor Unit.")
    c.drawString(480, altura - 160, "Total")
    c.line(50, altura - 165, 550, altura - 165)

    y = altura - 185
    total_geral = 0

    c.setFont("Helvetica", 12)
    for produto in produtos:
        total = produto["qtd"] * produto["valor"]
        total_geral += total
        c.drawString(50, y, produto["nome"])
        c.drawString(300, y, str(produto["qtd"]))
        c.drawString(380, y, f"R$ {produto['valor']:.2f}")
        c.drawString(480, y, f"R$ {total:.2f}")
        y -= 20

    c.line(50, y - 5, 550, y - 5)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(380, y - 20, "TOTAL:")
    c.drawString(480, y - 20, f"R$ {total_geral:.2f}")
    c.save()

    salvar_orcamento(cliente, total_geral)
    return nome_arquivo, total_geral

# Interface
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Gerador de Orçamentos")
        self.geometry("600x600")
        self.produtos = []
        self.criar_interface()

    def criar_interface(self):
        # Cliente
        ttk.Label(self, text="Nome do Cliente:", font=("Helvetica", 12)).pack(pady=(20, 5))
        self.entry_cliente = ttk.Entry(self, width=40, font=("Helvetica", 12))
        self.entry_cliente.pack()

        # Produto
        ttk.Label(self, text="Produto:", font=("Helvetica", 12)).pack(pady=(15, 5))
        self.entry_produto = ttk.Entry(self, width=40, font=("Helvetica", 12))
        self.entry_produto.pack()

        # Quantidade e Valor
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Label(frame, text="Qtd:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.entry_qtd = ttk.Entry(frame, width=10, font=("Helvetica", 12))
        self.entry_qtd.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Valor Unit. (R$):", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.entry_valor = ttk.Entry(frame, width=10, font=("Helvetica", 12))
        self.entry_valor.grid(row=0, column=3, padx=5)

        # Botão adicionar produto
        ttk.Button(self, text="Adicionar Produto", bootstyle=INFO,
                   command=self.adicionar_produto).pack(pady=5)

        # Lista de produtos
        self.lista = ttk.Treeview(self, columns=("produto", "qtd", "valor", "total"),
                                   show="headings", height=8)
        self.lista.heading("produto", text="Produto")
        self.lista.heading("qtd", text="Qtd")
        self.lista.heading("valor", text="Valor Unit.")
        self.lista.heading("total", text="Total")
        self.lista.column("produto", width=220)
        self.lista.column("qtd", width=60)
        self.lista.column("valor", width=100)
        self.lista.column("total", width=100)
        self.lista.pack(pady=10, padx=20)

        # Total
        self.label_total = ttk.Label(self, text="Total: R$ 0.00", font=("Helvetica", 14, "bold"))
        self.label_total.pack()

        # Botão gerar
        ttk.Button(self, text="Gerar Orçamento PDF", bootstyle=SUCCESS,
                   command=self.gerar).pack(pady=15)

        # Status
        self.label_status = ttk.Label(self, text="", font=("Helvetica", 11))
        self.label_status.pack()

    def adicionar_produto(self):
        nome = self.entry_produto.get()
        qtd = self.entry_qtd.get()
        valor = self.entry_valor.get()

        if not nome or not qtd or not valor:
            self.label_status.config(text="Preencha todos os campos do produto.", bootstyle=DANGER)
            return

        try:
            qtd = int(qtd)
            valor = float(valor.replace(",", "."))
        except:
            self.label_status.config(text="Qtd deve ser número inteiro e valor deve ser número.", bootstyle=DANGER)
            return

        total = qtd * valor
        self.produtos.append({"nome": nome, "qtd": qtd, "valor": valor})
        self.lista.insert("", END, values=(nome, qtd, f"R$ {valor:.2f}", f"R$ {total:.2f}"))

        total_geral = sum(p["qtd"] * p["valor"] for p in self.produtos)
        self.label_total.config(text=f"Total: R$ {total_geral:.2f}")

        self.entry_produto.delete(0, END)
        self.entry_qtd.delete(0, END)
        self.entry_valor.delete(0, END)
        self.label_status.config(text="Produto adicionado!", bootstyle=SUCCESS)

    def gerar(self):
        cliente = self.entry_cliente.get()
        if not cliente:
            self.label_status.config(text="Digite o nome do cliente.", bootstyle=DANGER)
            return
        if not self.produtos:
            self.label_status.config(text="Adicione pelo menos um produto.", bootstyle=DANGER)
            return

        arquivo, total = gerar_pdf(cliente, self.produtos)
        self.label_status.config(text=f"PDF gerado: {arquivo} | Total: R$ {total:.2f}", bootstyle=SUCCESS)
        self.produtos = []
        for item in self.lista.get_children():
            self.lista.delete(item)
        self.label_total.config(text="Total: R$ 0.00")
        self.entry_cliente.delete(0, END)

criar_banco()
app = App()
app.mainloop()