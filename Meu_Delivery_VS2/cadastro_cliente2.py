import tkinter as tk
from tkinter import messagebox
import sqlite3
import database2 # Garantindo o import do arquivo correto

class JanelaCadastro(tk.Toplevel):
    def __init__(self, master, dados_cliente=None): # Adicionado parâmetro opcional para edição
        super().__init__(master)
        self.title("Gerenciar Cliente")
        self.geometry("350x550")
        self.configure(bg="#f4f7f6")
        self.cliente_id = None # Controla se é um novo cadastro ou edição

        # 1. Configuração de Interface (Labels e Entradas)
        tk.Label(self, text="Nome:", bg="#f4f7f6").pack(pady=5)
        self.ent_nome = tk.Entry(self, font=("Arial", 12))
        self.ent_nome.pack(pady=5, padx=20, fill="x")

        tk.Label(self, text="Telefone:", bg="#f4f7f6").pack(pady=5)
        self.ent_tel = tk.Entry(self, font=("Arial", 12))
        self.ent_tel.pack(pady=5, padx=20, fill="x")

        tk.Label(self, text="Endereço:", bg="#f4f7f6").pack(pady=5)
        self.ent_end = tk.Entry(self, font=("Arial", 12))
        self.ent_end.pack(pady=5, padx=20, fill="x")

        # 2. Seleção de Status (Inativo adicionado para condizer com database2)
        tk.Label(self, text="Tipo de Cliente / Status:", bg="#c2e7db").pack(pady=5)
        self.var_status = tk.StringVar(self)
        self.var_status.set("Comum") 
        
        # Lista de opções incluindo a lógica de Inativo do database2
        opcoes_status = ["Comum", "Idoso", "PCD", "Inativo"]
        self.opt_status = tk.OptionMenu(self, self.var_status, *opcoes_status)
        self.opt_status.config(font=("Arial", 10), bg="white")
        self.opt_status.pack(pady=5, padx=20, fill="x")

        # 3. Botão de Ação
        self.btn_salvar = tk.Button(self, text="Salvar Cliente", bg="#28a745", fg="white", 
                                   command=self.salvar, font=("Arial", 10, "bold"))
        self.btn_salvar.pack(pady=30)

        # 4. Lógica de Preenchimento para Edição
        if dados_cliente:
            self.preencher_dados(dados_cliente)

    def preencher_dados(self, dados):
        """Preenche os campos quando a janela é aberta para edição"""
        self.cliente_id = dados[0]
        self.ent_nome.insert(0, dados[1])
        self.ent_tel.insert(0, dados[2])
        self.ent_end.insert(0, dados[3])
        self.var_status.set(dados[4])
        self.btn_salvar.config(text="Atualizar Dados", bg="#007bff")

    def salvar(self):
        """Coleta os dados e decide entre salvar_cliente ou atualizar_cliente"""
        nome = self.ent_nome.get().strip()
        tel = self.ent_tel.get().strip()
        end = self.ent_end.get().strip()
        status = self.var_status.get()

        if nome and tel and end:
            try:
                if self.cliente_id:
                    # Se existe ID, chama a função de manutenção (Update)
                    database2.atualizar_cliente(self.cliente_id, nome, tel, end, status)
                    messagebox.showinfo("Sucesso", "Cadastro atualizado!")
                else:
                    # Se não existe ID, chama a função de inserção (Insert)
                    database2.salvar_cliente(nome, tel, end, status)
                    messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado!")
                
                self.destroy() 
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Este telefone já está cadastrado!")
            except Exception as e:
                messagebox.showerror("Erro Crítico", f"Erro: {e}")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaCadastro(root)
    root.mainloop()