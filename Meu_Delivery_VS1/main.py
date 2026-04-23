import tkinter as tk
from tkinter import messagebox, ttk
import database  
from gerar_pedido import JanelaPedido

class JanelaCadastro:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Novo Cliente")
        self.top.geometry("350x300")
        self.top.grab_set()

        tk.Label(self.top, text="Nome:").pack(pady=5)
        self.ent_nome = tk.Entry(self.top, width=30); self.ent_nome.pack()

        tk.Label(self.top, text="Telefone:").pack(pady=5)
        self.ent_tel = tk.Entry(self.top, width=30); self.ent_tel.pack()

        tk.Label(self.top, text="Endereço:").pack(pady=5)
        self.ent_endereco = tk.Entry(self.top, width=30); self.ent_endereco.pack()

        tk.Button(self.top, text="Salvar", bg="#28a745", fg="white", command=self.confirmar).pack(pady=20)

    def confirmar(self):
        n, t, e = self.ent_nome.get(), self.ent_tel.get(), self.ent_endereco.get()
        if n and t and e:
            database.salvar_cliente(n, t, e)
            messagebox.showinfo("Sucesso", "Cadastrado!")
            self.top.destroy()
        else: messagebox.showwarning("Erro", "Preencha tudo!")

class SistemaJAD:
    def __init__(self, root):
        self.root = root
        self.root.title("***** Sistema JAD SQlite *****")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f6f9")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="*** Controle de Delivery ***", font=("Arial", 18, "bold"), bg="#f4f6f9").pack(pady=20)
        frame = tk.Frame(self.root, bg="#f4f6f9"); frame.pack(pady=10)
        
        btn_c = {"width": 15, "height": 2, "fg": "white", "font": ("Arial", 9, "bold")}
        tk.Button(frame, text="Cadastrar Cliente", command=lambda: JanelaCadastro(self.root), bg="#007bff", **btn_c).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Ver Clientes", command=self.exibir_clientes, bg="#17a2b8", **btn_c).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Gerar Pedido", command=lambda: JanelaPedido(self.root), bg="#28a745", **btn_c).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Ver Pedidos", command=self.exibir_pedidos, bg="#ffc107", fg="black", font=btn_c["font"], width=15, height=2).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Sair", command=self.root.destroy, bg="#dc3545", **btn_c).grid(row=0, column=4, padx=5)

        self.tree_frame = tk.Frame(self.root); self.tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree = ttk.Treeview(self.tree_frame, columns=("id", "nome", "telefone", "endereco"), show="headings")
        self.tree.heading("id", text="ID"); self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone"); self.tree.heading("endereco", text="Endereço")
        self.tree.pack(fill="both", expand=True)

    def exibir_clientes(self):
        self.tree["columns"] = ("id", "nome", "telefone", "endereco")
        for c in self.tree["columns"]: self.tree.heading(c, text=c.capitalize())
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in database.listar_clientes(): self.tree.insert("", "end", values=c)

    def exibir_pedidos(self):
        self.tree["columns"] = ("id", "cliente", "valor", "data")
        self.tree.heading("id", text="Nº"); self.tree.heading("cliente", text="Cliente")
        self.tree.heading("valor", text="R$"); self.tree.heading("data", text="Data")
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in database.listar_pedidos(): self.tree.insert("", "end", values=p)

if __name__ == "__main__":
    root = tk.Tk(); app = SistemaJAD(root); root.mainloop()