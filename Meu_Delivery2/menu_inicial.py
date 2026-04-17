import tkinter as tk
from tkinter import messagebox, ttk
import database2  
from cadastro_cliente2 import JanelaCadastro 
from gerar_pedido2 import JanelaPedido # Importação do novo script de pedidos

class SistemaJAD:
    def __init__(self, root):
        self.root = root
        self.root.title("***** Sistema JAD - SQLite *****")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f4f6f9")
        
        self.setup_ui()
        
        # Tags de Cores (Rigorosamente mantidas conforme solicitado)
        self.tree.tag_configure('inativo', background='black', foreground='white') 
        self.tree.tag_configure('finalizado', background="#ee0e06", foreground='white') 
        self.tree.tag_configure('prioridade', foreground='blue', font=('Arial', 9, 'bold'))

        self.exibir_clientes()

    def setup_ui(self):
        tk.Label(self.root, text="--- Controle de Delivery JAD ---", 
                 font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#333").pack(pady=10)

        frame_busca = tk.Frame(self.root, bg="#f4f6f9")
        frame_busca.pack(fill="x", padx=40)
        
        tk.Label(frame_busca, text="Buscar:", bg="#f4f6f9", font=("Arial", 10, "bold")).pack(side="left")
        self.ent_busca = tk.Entry(frame_busca, font=("Arial", 11))
        self.ent_busca.pack(side="left", padx=10, fill="x", expand=True)
        self.ent_busca.bind("<KeyRelease>", self.filtrar_dados) 

        frame_menu = tk.Frame(self.root, bg="#f4f6f9")
        frame_menu.pack(pady=15)
        
        btn_style = {"width": 15, "height": 2, "fg": "white", "font": ("Arial", 9, "bold")}

        # --- BOTÕES DE CLIENTES ---
        tk.Button(frame_menu, text="Novo Cliente", bg="#28a745", **btn_style, 
                  command=self.abrir_cadastro).grid(row=0, column=0, padx=5)
        tk.Button(frame_menu, text="Editar", bg="#007bff", **btn_style, 
                  command=self.editar_selecionado).grid(row=0, column=1, padx=5)
        tk.Button(frame_menu, text="Ver Clientes", bg="#6c757d", **btn_style, 
                  command=self.exibir_clientes).grid(row=0, column=2, padx=5)
        
        # --- BOTÕES DE PEDIDOS ---
        tk.Button(frame_menu, text="Ver Pedidos", bg="#ffe607", fg="black", font=btn_style["font"], 
                  width=btn_style["width"], height=btn_style["height"], 
                  command=self.exibir_pedidos).grid(row=0, column=3, padx=5)   
        
        # Chama a função que abre o script gerar_pedido2
        tk.Button(frame_menu, text="Gerar Pedido", bg="#fd0505", **btn_style, 
                  command=self.abrir_pedido).grid(row=0, column=4, padx=5)       
        
        tk.Button(frame_menu, text="Sair", bg="#000000", **btn_style, 
                  command=self.confirmar_saida).grid(row=0, column=5, padx=5)
 
        self.tree_frame = tk.Frame(self.root, bg="white")
        self.tree_frame.pack(fill="both", expand=True, padx=40, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", columns=("id", "col1", "col2", "col3", "status"), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrol = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrol.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrol.set)

        self.lbl_total = tk.Label(self.root, text="", font=("Arial", 11, "bold"), bg="#f4f6f9", fg="#28a745")
        self.lbl_total.pack(pady=10)

    def filtrar_dados(self, event):
        termo = self.ent_busca.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.tree.heading("col1")["text"] == "Nome":
            dados = database2.listar_clientes()
        else:
            dados = database2.listar_pedidos()

        for d in dados:
            if termo in str(d[1]).lower() or termo in str(d[2]).lower():
                tag = ""
                if "Inativo" in str(d): tag = "inativo"
                if "Finalizado" in str(d): tag = "finalizado"
                if "Idoso" in str(d) or "PCD" in str(d): tag = "prioridade"
                self.tree.insert("", "end", values=d, tags=(tag,))

    def exibir_clientes(self):
        self.lbl_total.config(text="") 
        self.tree["columns"] = ("id", "nome", "telefone", "endereco", "status")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize(), anchor="center")
            self.tree.column(col, width=150, anchor="center")
        
        self.tree.column("id", width=50, anchor="center")
        for item in self.tree.get_children(): self.tree.delete(item)
            
        for c in database2.listar_clientes():
            tag = "inativo" if c[4] == "Inativo" else ""
            if c[4] in ["Idoso", "PCD"]: tag = "prioridade"
            self.tree.insert("", "end", values=c, tags=(tag,))

    def exibir_pedidos(self):
        self.tree["columns"] = ("id", "cliente", "valor", "data", "status")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize(), anchor="center")
            self.tree.column(col, width=150, anchor="center")
        
        for item in self.tree.get_children(): self.tree.delete(item)
            
        total_vendas = 0
        for p in database2.listar_pedidos():
            total_vendas += p[2] 
            tag = "finalizado" if p[4] == "Finalizado" else ""
            self.tree.insert("", "end", values=p, tags=(tag,))
        
        self.lbl_total.config(text=f"Total em Pedidos: R$ {total_vendas:.2f}")

    def abrir_cadastro(self):
        janela = JanelaCadastro(self.root)
        self.root.wait_window(janela)
        self.exibir_clientes()

    def editar_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado: 
            return messagebox.showwarning("Aviso", "Selecione um item!")
        dados = self.tree.item(selecionado)["values"]
        try:
            if self.tree.heading(self.tree["columns"][1])["text"] == "Nome":
                janela = JanelaCadastro(self.root, dados_cliente=dados)
                self.root.wait_window(janela)
                self.exibir_clientes()
            else:
                messagebox.showinfo("Info", "Para editar pedidos, use o sistema de finalização.")
        except Exception as e:
            messagebox.showerror("Erro", "Não foi possível identificar a seleção.")

    def abrir_pedido(self):
        # Chama a classe JanelaPedido importada de gerar_pedido2.py
        janela = JanelaPedido(self.root)
        self.root.wait_window(janela.top)
        self.exibir_pedidos()
        
    def concluir_pedido(self):
        selecionado = self.tree.selection()
        if not selecionado: return
        id_p = self.tree.item(selecionado)["values"][0]
        if messagebox.askyesno("Confirmar", "Finalizar este pedido?"):
            database2.atualizar_status_pedido(id_p, "Finalizado")
            self.exibir_pedidos()

    def confirmar_saida(self):
        if messagebox.askyesno("Sair", "Encerrar sistema?"): self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaJAD(root)
    root.mainloop()