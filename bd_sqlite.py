import sqlite3

DB_NAME = "tarefas.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    return conn


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Executa automaticamente ao importar
criar_tabela()
