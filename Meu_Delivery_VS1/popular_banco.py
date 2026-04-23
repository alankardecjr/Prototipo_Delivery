import database
import sqlite3

def popular_banco():
    # 1. Conecta ao banco e garante que as tabelas existam
    database.criar_tabelas()
    conn = database.conectar()
    cursor = conn.cursor()

    print("--- Iniciando Povoamento do Banco de Dados ---")

    # 2. Lista de 10 Clientes Fictícios (Nome, Telefone, Endereço)
    clientes = [
        ('Ricardo Oliveira', '(11) 98888-1111', 'Rua das Palmeiras, 120'),
        ('Fernanda Souza', '(11) 97777-2222', 'Av. Paulista, 1500 - Ap 32'),
        ('Marcos Silveira', '(21) 96666-3333', 'Rua Rio Branco, 45'),
        ('Juliana Costa', '(31) 95555-4444', 'Rua da Bahia, 300'),
        ('Roberto Carlos', '(11) 94444-5555', 'Av. Brasil, 1010'),
        ('Luciana Melo', '(11) 93333-6666', 'Rua Augusta, 2500'),
        ('Bruno Henrique', '(21) 92222-7777', 'Rua Flamengo, 80'),
        ('Camila Rodrigues', '(41) 91111-8888', 'Rua Curitiba, 777'),
        ('Gabriel Jesus', '(11) 90000-9999', 'Av. das Nações, 400'),
        ('Beatriz Nunes', '(11) 98765-4321', 'Rua das Flores, 99')
    ]

    # 3. Lista de 8 Produtos Variados (Nome, Preço, Categoria)
    produtos = [
        ('X-Tudo Especial', 32.50, 'Lanches'),
        ('Cachorro Quente Duplo', 18.00, 'Lanches'),
        ('Pizza Brotinho Muçarela', 25.00, 'Pizzas'),
        ('Batata Frita com Queijo', 22.00, 'Porções'),
        ('Anéis de Cebola', 15.50, 'Porções'),
        ('Refrigerante Lata 350ml', 6.00, 'Bebidas'),
        ('Suco de Laranja 500ml', 10.00, 'Bebidas'),
        ('Pudim de Leite', 12.00, 'Sobremesas')
    ]

    # Inserindo Clientes
    print("\nInserindo Clientes...")
    for c in clientes:
        try:
            cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", c)
            print(f"Sucedido: {c[0]}")
        except sqlite3.IntegrityError:
            print(f"Aviso: Cliente {c[0]} já existe (telefone duplicado).")

    # Inserindo Produtos
    print("\nInserindo Produtos no Cardápio...")
    for p in produtos:
        # Verifica se o produto já existe pelo nome para não duplicar
        cursor.execute("SELECT id FROM itens WHERE nome = ?", (p[0],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO itens (nome, preco, categoria) VALUES (?, ?, ?)", p)
            print(f"Sucedido: {p[0]}")
        else:
            print(f"Aviso: Produto {p[0]} já existe.")

    conn.commit()
    conn.close()
    print("\n✅ Banco de dados 'delivery.db' populado com sucesso!")

if __name__ == "__main__":
    popular_banco()