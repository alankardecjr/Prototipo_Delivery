import sqlite3

def conectar():
    """Conecta ao banco de dados delivery.db"""
    return sqlite3.connect("delivery.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Tabela de Produtos (Cardápio)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        categoria TEXT
    )""")

    # 2. Tabela de Clientes (Nome, Telefone, Endereço)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT UNIQUE NOT NULL,
        endereco TEXT NOT NULL
    )""")

    # 3. Tabela de Pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_nome TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, endereco FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return dados

def salvar_cliente(nome, telefone, endereco):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", 
                       (nome, telefone, endereco))
        conn.commit()
    finally:
        conn.close()

def listar_itens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens")
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente_nome, valor, data FROM pedidos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# Inicializa as tabelas ao ser importado
criar_tabelas()