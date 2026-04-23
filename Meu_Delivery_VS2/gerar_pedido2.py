import tkinter as tk
from tkinter import messagebox, ttk
import database2  # Importa seu banco de dados atualizado

class JanelaPedido:
    """Interface de pedidos integrada ao banco de dados SQLite."""

    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("***** Sistema JAD Delivery *****")
        self.top.geometry("900x750") 
        self.top.configure(bg="#f4f7f6")
        self.top.grab_set() 

        # Estado do pedido
        self.pedido_atual = []
        self.total_valor = 0.0
        self.clientes_dict = {}

        self.setup_ui()

    def setup_ui(self):
        # --- Título ---
        tk.Label(self.top, text="--- Registro de Pedidos ---", font=("Arial", 18, "bold"), bg="#f4f7f6").pack(pady=10)

        # --- Seleção de Cliente ---
        cliente_frame = tk.Frame(self.top, bg="#f4f7f6")
        cliente_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(cliente_frame, text="Selecione o Cliente:", font=("Arial", 10, "bold"), bg="#f4f7f6").pack(side="left")
        
        self.combo_clientes = ttk.Combobox(cliente_frame, state="readonly", width=50, font=("Arial", 11))
        self.combo_clientes.pack(side="left", padx=10)
        self.carregar_clientes()

        # --- Frame Principal ---
        main_frame = tk.Frame(self.top, bg="#f4f7f6")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Coluna Esquerda: Cardápio ---
        self.menu_frame = tk.LabelFrame(main_frame, text="Cardápio (Clique para Adicionar)", padx=10, pady=10, bg="white")
        self.menu_frame.pack(side="left", fill="both", expand=True)
        
        canvas = tk.Canvas(self.menu_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.menu_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.atualizar_botoes_menu()

        # --- Coluna Direita: Resumo ---
        resumo_frame = tk.LabelFrame(main_frame, text="Itens Selecionados", padx=10, pady=10, bg="white")
        resumo_frame.pack(side="right", fill="both", expand=True)

        self.lista_pedido = tk.Listbox(resumo_frame, font=("Arial", 11), borderwidth=0)
        self.lista_pedido.pack(fill="both", expand=True)

        self.label_total = tk.Label(resumo_frame, text="Total: R$ 0.00", font=("Arial", 16, "bold"), fg="#28a745", bg="white")
        self.label_total.pack(pady=10)

        # --- Botões de Ação ---
        tk.Button(resumo_frame, text="Remover Último Item", command=self.remover_ultimo, 
                  bg="#ffc107", fg="black", font=("Arial", 9, "bold")).pack(fill="x", pady=2)

        tk.Button(resumo_frame, text="Finalizar e Salvar", command=self.finalizar_pedido, 
                  bg="#28a745", fg="white", font=("Arial", 10, "bold"), height=2).pack(fill="x", pady=5)

        # --- Botão Sair ---
        tk.Button(resumo_frame, text="Cancelar e Sair", command=self.confirmar_saida, 
                  bg="#dc3545", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=5)

    def carregar_clientes(self):
        try:
            clientes = database2.listar_clientes_ativos()
            nomes = []
            for c in clientes:
                nome_exibicao = f"{c[0]} - {c[1]} ({c[4]})"
                nomes.append(nome_exibicao)
                self.clientes_dict[nome_exibicao] = c[0]
            self.combo_clientes['values'] = nomes
        except:
            self.combo_clientes['values'] = ["Erro ao carregar clientes"]

    def atualizar_botoes_menu(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        try:
            itens_cardapio = database2.listar_itens()
            for item in itens_cardapio:
                nome, preco = item[1], item[2]
                btn = tk.Button(self.scrollable_frame, text=f"{nome}\nR$ {preco:.2f}", 
                                bg="#f8f9fa", width=20, height=3, 
                                command=lambda n=nome, p=preco: self.adicionar_item(n, p))
                btn.pack(pady=5, fill="x")
        except:
            tk.Label(self.scrollable_frame, text="Erro ao carregar cardápio", bg="white").pack()

    def adicionar_item(self, nome, preco):
        self.pedido_atual.append((nome, preco))
        self.lista_pedido.insert(tk.END, f" {nome} - R$ {preco:.2f}")
        self.atualizar_total()

    def remover_ultimo(self):
        if self.pedido_atual:
            self.pedido_atual.pop()
            self.lista_pedido.delete(tk.END)
            self.atualizar_total()

    def atualizar_total(self):
        self.total_valor = sum(item[1] for item in self.pedido_atual)
        self.label_total.config(text=f"Total: R$ {self.total_valor:.2f}")

    def finalizar_pedido(self):
        cliente_fmt = self.combo_clientes.get()
        if not cliente_fmt or not self.pedido_atual:
            messagebox.showwarning("Aviso", "Selecione um cliente e adicione itens!")
            return
        try:
            id_cliente = self.clientes_dict[cliente_fmt]
            database2.salvar_pedido(id_cliente, self.total_valor)
            messagebox.showinfo("Sucesso", f"Pedido salvo para {cliente_fmt}!")
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def confirmar_saida(self):
        if self.pedido_atual:
            pergunta = "Você tem itens no carrinho. Deseja realmente cancelar o pedido e sair?"
        else:
            pergunta = "Deseja fechar a janela de pedido?"
        if messagebox.askyesno("Confirmar Saída", pergunta):
            self.top.destroy()