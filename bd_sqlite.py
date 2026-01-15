import sqlite3
import os
import sys


def caminho_db():
    if getattr(sys, 'frozen', False):
        # executando como .exe
        pasta_base = os.path.dirname(sys.executable)
    else:
        # executando como script .py
        pasta_base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(pasta_base, "tarefas.db")


def conectar():
    conn = sqlite3.connect(caminho_db())
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


def listar_tarefas(tar_stt=None):
    """
    Lista tarefas do banco SQLite.
    Se tar_stt for informado, filtra pelo status.
    """
    conn = conectar()
    cursor = conn.cursor()

    if tar_stt is None or tar_stt == "Todos":
        cursor.execute("""
            SELECT tar_id, tar_tit, tar_desc, tar_stt
            FROM tarefas
        """)
    else:
        cursor.execute("""
            SELECT tar_id, tar_tit, tar_desc, tar_stt
            FROM tarefas
            WHERE tar_stt = ?
        """, (tar_stt,))

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


def atualizar_tarefa(tar_id, tar_tit, tar_desc, tar_stt):
    """
    Atualiza uma tarefa existente no banco SQLite.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET tar_tit = ?, tar_desc = ?, tar_stt = ?
        WHERE tar_id = ?
    """, (tar_tit, tar_desc, tar_stt, tar_id))

    conn.commit()
    conn.close()



def tarefa_existe_pendente(tar_tit):
    """
    Verifica se já existe uma tarefa pendente com o mesmo título.
    Retorna True ou False.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM tarefas
        WHERE tar_tit = ?
        AND tar_stt = 'Pendente'
        LIMIT 1
    """, (tar_tit,))

    existe = cursor.fetchone() is not None

    conn.close()
    return existe



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
