import sqlite3

SQLITE_DB = "tarefas.db"

def conectar():
    conn = sqlite3.connect(SQLITE_DB)
    return conn


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            tar_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tar_tit TEXT NOT NULL,
            tar_desc TEXT NOT NULL,
            tar_stt TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def inserir_tarefa(tar_tit, tar_desc, tar_stt):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tarefas (tar_tit, tar_desc, tar_stt) VALUES(?, ?, ?)""", (tar_tit, tar_desc, tar_stt))

    conn.commit()
    conn.close()


def listar_tarefas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT tar_id, tar_tit, tar_desc, tar_stt FROM tarefas""")

    tarefas = cursor.fetchall()
    conn.close()

    return tarefas


def excluir_tarefa(tar_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tarefas WHERE tar_id = ?", (tar_id,))

    conn.commit()
    conn.close()


def limpar_tarefas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tarefas")

    conn.commit()
    conn.close()


# Executa automaticamente ao importar
criar_tabela()


# Teste manual do SQLite
if __name__ == "__main__":
    
    limpar_tarefas() 
    inserir_tarefa("Tarefa de teste", "SQLite funcionando", "Pendente")

    tarefas = listar_tarefas()
    print("Tarefas no banco:")

    for t in tarefas:
        print(t)

