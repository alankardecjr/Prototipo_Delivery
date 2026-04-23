import tkinter as tk
from tkinter import messagebox
import database

class JanelaCadastro(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastrar Cliente")
        self.geometry("350x400")
        self.configure(bg="#f4f7f6")
        
        tk.Label(self, text="Nome:", bg="#f4f7f6").pack(pady=5)
        self.ent_nome = tk.Entry(self, font=("Arial", 12))
        self.ent_nome.pack(pady=5, padx=20, fill="x")

        tk.Label(self, text="Telefone:", bg="#f4f7f6").pack(pady=5)
        self.ent_tel = tk.Entry(self, font=("Arial", 12))
        self.ent_tel.pack(pady=5, padx=20, fill="x")

        tk.Label(self, text="Endereço:", bg="#f4f7f6").pack(pady=5)
        self.ent_end = tk.Entry(self, font=("Arial", 12))
        self.ent_end.pack(pady=5, padx=20, fill="x")

        tk.Button(self, text="Salvar Cliente", bg="#28a745", fg="white", 
                  command=self.salvar, font=("Arial", 10, "bold")).pack(pady=20)

    def salvar(self):
        nome = self.ent_nome.get()
        tel = self.ent_tel.get()
        end = self.ent_end.get()

        if nome and tel and end:
            try:
                conn = database.conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", 
                               (nome, tel, end))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")
                self.destroy()
            except:
                messagebox.showerror("Erro", "Telefone já cadastrado!")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")