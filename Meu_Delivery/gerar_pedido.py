import tkinter as tk
from tkinter import messagebox, ttk
import database  # Importa seu banco de dados SQLite

class JanelaPedido:
    """Interface de pedidos integrada ao banco de dados SQLite."""

    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Gerar Novo Pedido - JAD")
        self.top.geometry("800x650")
        self.top.grab_set() # Foca na janela de pedido

        # Estado do pedido
        self.pedido_atual = []
        self.total_valor = 0.0

        self.setup_ui()

    def setup_ui(self):
        # --- Título ---
        tk.Label(self.top, text="Registro de Pedidos Delivery", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Seleção de Cliente (Novo Campo necessário para o Banco) ---
        cliente_frame = tk.Frame(self.top)
        cliente_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(cliente_frame, text="Selecione o Cliente:", font=("Arial", 10, "bold")).pack(side="left")
        
        self.combo_clientes = ttk.Combobox(cliente_frame, state="readonly", width=50)
        self.combo_clientes.pack(side="left", padx=10)
        self.carregar_clientes()

        # --- Frame Principal ---
        main_frame = tk.Frame(self.top)
        main_frame.pack(fill="both", expand=True, padx=20)

        # --- Coluna Esquerda: Menu de Seleção (Vindo do Banco) ---
        self.menu_frame = tk.LabelFrame(main_frame, text="Cardápio (Clique para Adicionar)", padx=10, pady=10)
        self.menu_frame.pack(side="left", fill="both", expand=True)
        
        # Scrollbar para o menu caso tenha muitos itens
        canvas = tk.Canvas(self.menu_frame)
        scrollbar = ttk.Scrollbar(self.menu_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.atualizar_botoes_menu()

        # --- Coluna Direita: Resumo do Pedido ---
        resumo_frame = tk.LabelFrame(main_frame, text="Resumo do Pedido", padx=10, pady=10)
        resumo_frame.pack(side="right", fill="both", expand=True)

        self.lista_pedido = tk.Listbox(resumo_frame, font=("Arial", 11))
        self.lista_pedido.pack(fill="both", expand=True)

        self.label_total = tk.Label(resumo_frame, text="Total: R$ 0.00", font=("Arial", 14, "bold"), fg="green")
        self.label_total.pack(pady=10)

        # --- Botões de Ação ---
        btn_remover = tk.Button(resumo_frame, text="Remover Último Item", command=self.remover_ultimo, bg="#ffcccb")
        btn_remover.pack(fill="x", pady=2)

        btn_finalizar = tk.Button(resumo_frame, text="Finalizar e Salvar no Banco", command=self.finalizar_pedido, bg="#90ee90", font=("Arial", 10, "bold"))
        btn_finalizar.pack(fill="x", pady=5)

    def carregar_clientes(self):
        """Busca nomes dos clientes no banco para o Combobox."""
        try:
            clientes = database.listar_clientes()
            # Pega apenas o nome (índice 1) de cada cliente
            nomes = [c[1] for c in clientes]
            self.combo_clientes['values'] = nomes
        except:
            self.combo_clientes['values'] = ["Nenhum cliente cadastrado"]

    def atualizar_botoes_menu(self):
        """Cria botões baseados na tabela 'itens' do banco de dados."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            itens_cardapio = database.listar_itens()
            for item in itens_cardapio:
                # item[1] = nome, item[2] = preco
                nome, preco = item[1], item[2]
                btn = tk.Button(self.scrollable_frame, text=f"{nome}\nR$ {preco:.2f}", 
                                width=20, height=3, command=lambda p=nome, v=preco: self.adicionar_item(p, v))
                btn.pack(pady=5, fill="x")
        except:
            tk.Label(self.scrollable_frame, text="Erro ao carregar cardápio").pack()

    def adicionar_item(self, nome, preco):
        self.pedido_atual.append((nome, preco))
        self.lista_pedido.insert(tk.END, f"{nome} - R$ {preco:.2f}")
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
        cliente_selecionado = self.combo_clientes.get()
        
        if not cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        
        if not self.pedido_atual:
            messagebox.showwarning("Aviso", "O pedido está vazio!")
            return

        try:
            # Salva no SQLite através do database.py
            # A função no database deve aceitar (cliente_nome, valor_total)
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pedidos (cliente_nome, valor) VALUES (?, ?)", 
                           (cliente_selecionado, self.total_valor))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Pedido de R$ {self.total_valor:.2f} salvo para {cliente_selecionado}!")
            self.top.destroy() # Fecha a janela após salvar
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar pedido no banco: {e}")

if __name__ == "__main__":
    # Apenas para teste isolado
    root = tk.Tk()
    app = JanelaPedido(root)
    root.mainloop()