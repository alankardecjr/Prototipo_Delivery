import sqlite3

def conectar():
    """Conecta ao banco de dados delivery2.db"""
    return sqlite3.connect("delivery2.db")

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

    # 2. Tabela de Clientes (Status padrão: Ativo)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT UNIQUE NOT NULL,
        endereco TEXT NOT NULL,
        status TEXT DEFAULT 'Ativo'
    )""")

    # 3. Tabela de Pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        valor_total REAL NOT NULL,
        data TEXT DEFAULT (datetime('now', 'localtime')),
        status TEXT DEFAULT 'pendente',
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )""")
    
    conn.commit()
    conn.close()

# --- FUNÇÕES PARA CLIENTES (CRUD & MANUTENÇÃO) ---

def salvar_cliente(nome, telefone, endereco, status='Ativo'):
    """Insere um novo cliente no banco de dados"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, endereco, status) 
            VALUES (?, ?, ?, ?)""", (nome, telefone, endereco, status))    
        conn.commit()
    finally:
        conn.close()

def atualizar_cliente(id_cliente, nome, telefone, endereco, status):
    """Atualiza os dados de um cliente existente pelo ID"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE clientes 
            SET nome = ?, telefone = ?, endereco = ?, status = ? 
            WHERE id = ?""", (nome, telefone, endereco, status, id_cliente))
        conn.commit()
    finally:
        conn.close()

def alterar_status_cliente(id_cliente, novo_status):
    """Altera o status do cliente (ex: Ativo/Inativo/Idoso/PCD)"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE clientes SET status = ? WHERE id = ?", (novo_status, id_cliente))
        conn.commit()
    finally:
        conn.close()

# --- FUNÇÕES DE CONSULTA DE CLIENTES ---

def listar_clientes():
    """Retorna todos os clientes para a tela de gestão"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, endereco, status FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_clientes_ativos():
    """Retorna apenas clientes que não estão inativos para a tela de pedidos"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, endereco, status FROM clientes WHERE status != 'Inativo'")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- FUNÇÕES PARA ITENS ---

def listar_itens():
    """Retorna todos os itens do cardápio"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- FUNÇÕES PARA PEDIDOS (CRUD) ---

def salvar_pedido(cliente_id, valor_total, status='pendente'):
    """Registra um novo pedido vinculado a um cliente"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pedidos (cliente_id, valor_total, status) 
            VALUES (?, ?, ?)""", (cliente_id, valor_total, status))
        conn.commit()
    finally:
        conn.close()

def atualizar_status_pedido(id_pedido, novo_status):
    """Atualiza o status do pedido (ex: pendente, finalizado, cancelado)"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, id_pedido))
        conn.commit()
    finally:
        conn.close()

def excluir_pedido(id_pedido):
    """Remove um pedido do banco de dados permanentemente"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
        conn.commit()
    finally:
        conn.close()

def listar_pedidos():
    """Retorna pedidos com nomes dos clientes usando JOIN"""
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT p.id, c.nome, p.valor_total, p.data, p.status, c.status 
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id 
    ORDER BY p.id DESC
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

# Inicializa o banco
criar_tabelas()