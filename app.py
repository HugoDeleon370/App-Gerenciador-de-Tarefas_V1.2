import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
# Importa apenas funções SQLite
from bd_sqlite import (
    inserir_tarefa,
    listar_tarefas,
    excluir_tarefa,
    atualizar_tarefa,
    tarefa_existe_pendente
)


class ger_tar_app:

    def __init__(self, root):

        self.root = root
        self.root.title("App")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("light")

        # -------------------------------------------------------------
        # TÍTULO DA TAREFA
        # -------------------------------------------------------------

        ctk.CTkLabel(
            root,
            text="Título da Tarefa:",
            font=("Arial bold", 15)
        ).grid(row=0, column=0, sticky="e", pady=15, padx=20)

        self.tit_tar = ctk.CTkEntry(
            root,
            width=445,
            border_width=1,
            border_color="#5e5e5e"
        )
        self.tit_tar.grid(row=0, column=1, pady=10)

        # -------------------------------------------------------------
        # DESCRIÇÃO DA TAREFA
        # -------------------------------------------------------------

        ctk.CTkLabel(
            root,
            text="Descrição da Tarefa:",
            font=("Arial bold", 15)
        ).grid(row=1, column=0, pady=10, sticky="n", padx=20)

        self.desc_tar = ctk.CTkTextbox(
            root,
            width=445,
            height=100,
            border_width=1,
            border_color="#5e5e5e"
        )
        self.desc_tar.grid(row=1, column=1, pady=10)

        # -------------------------------------------------------------
        # FUNÇÕES INTERNAS (CALLBACKS)
        # -------------------------------------------------------------

        def carregar_tarefas(status_filtro=None):
            """Carrega tarefas do SQLite na tabela"""

            self.tabela.delete(*self.tabela.get_children())

            tarefas = (
                listar_tarefas()
                if status_filtro in (None, "Todos")
                else listar_tarefas(status_filtro)
            )

            for tar_id, titulo, descricao, status in tarefas:
                self.tabela.insert(
                    "",
                    "end",
                    iid=str(tar_id),
                    values=(titulo, descricao, status)
                )

        def aplicar_filtro():
            carregar_tarefas(self.status_var.get())

        def limpar_campos():
            """Limpa campos de entrada e seleção"""
            self.tit_tar.delete(0, "end")
            self.desc_tar.delete("1.0", "end")
            self.status_var.set("Pendente")
            self.tabela.selection_remove(self.tabela.selection())

        def add_tar():
            titulo = self.tit_tar.get().strip()
            descricao = self.desc_tar.get("1.0", "end").strip()
            status = self.status_var.get()

            if status == "Todos":
                status = "Pendente"

            if not titulo or not descricao:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            # Validação de duplicidade (SQLite)
            if tarefa_existe_pendente(titulo):
                messagebox.showwarning(
                    "Tarefa existente",
                    f"Já existe uma tarefa pendente chamada '{titulo}'."
                )
                return

            if len(titulo) > 30 or len(descricao) > 150:
                messagebox.showwarning(
                    "Limite excedido",
                    "Título: 30 caracteres | Descrição: 150 caracteres."
                )
                return

            inserir_tarefa(titulo, descricao, status)
            carregar_tarefas("Todos")
            limpar_campos()

            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

        def up_tar():
            selecionado = self.tabela.selection()

            if not selecionado:
                messagebox.showwarning("Atenção", "Selecione uma tarefa.")
                return

            tar_id = selecionado[0]

            atualizar_tarefa(
                tar_id,
                self.tit_tar.get().strip(),
                self.desc_tar.get("1.0", "end").strip(),
                self.status_var.get()
            )

            carregar_tarefas("Todos")
            limpar_campos()

            messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")

        def del_tar():
            selecionado = self.tabela.selection()

            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma tarefa.")
                return

            excluir_tarefa(selecionado[0])
            carregar_tarefas("Todos")
            limpar_campos()

            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")

        def selecionar_tarefa(event):
            item = self.tabela.selection()
            if not item:
                return

            titulo, descricao, status = self.tabela.item(item, "values")

            self.tit_tar.delete(0, "end")
            self.tit_tar.insert(0, titulo)

            self.desc_tar.delete("1.0", "end")
            self.desc_tar.insert("1.0", descricao)

            self.status_var.set(status)

        # -------------------------------------------------------------
        # BOTÕES
        # -------------------------------------------------------------

        btn_frame = ctk.CTkFrame(root)
        btn_frame.grid(row=2, column=1, pady=15, sticky="w")

        ctk.CTkButton(btn_frame, text="Adicionar", command=add_tar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=up_tar).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", command=del_tar).grid(row=0, column=2, padx=5)

        # -------------------------------------------------------------
        # STATUS + FILTRO
        # -------------------------------------------------------------

        self.status_var = ctk.StringVar(value="Pendente")

        ctk.CTkOptionMenu(
            root,
            values=["Pendente", "Concluída", "Todos"],
            variable=self.status_var
        ).grid(row=3, column=1, sticky="w")

        ctk.CTkButton(
            root,
            text="Aplicar Filtro",
            command=aplicar_filtro
        ).grid(row=3, column=1, sticky="e", padx=30)

        # -------------------------------------------------------------
        # TABELA
        # -------------------------------------------------------------

        self.tabela = ttk.Treeview(
            root,
            columns=("Título", "Descrição", "Status"),
            show="headings"
        )

        self.tabela.heading("Título", text="Tarefa")
        self.tabela.heading("Descrição", text="Descrição")
        self.tabela.heading("Status", text="Status")

        self.tabela.grid(row=4, column=1, columnspan=3, pady=(15, 0))
        self.tabela.bind("<<TreeviewSelect>>", selecionar_tarefa)

        carregar_tarefas("Todos")


# -------------------------------------------------------------
# INICIALIZAÇÃO
# -------------------------------------------------------------

root = ctk.CTk()
app = ger_tar_app(root)
root.mainloop()
