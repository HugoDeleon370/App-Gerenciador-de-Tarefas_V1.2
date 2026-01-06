import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId
from bd_sqlite import inserir_tarefa, listar_tarefas


class ger_tar_app():

    def __init__(self, root):

        self.root = root
        self.tarefa_selecionada_id = None
        self.root.title("App")
        self.root.geometry("800x580")
        self.root.resizable(False, False) 
        ctk.set_appearance_mode("light")

        # Conexão com o banco de dados
        try:
            self.cliente = MongoClient("mongodb+srv://user_hd:tgYkDOOvW0WGdZaS@cluster0.yd1ejkl.mongodb.net/?appName=Cluster0") 
            self.bd = self.cliente["tarefas"]
            self.colecao = self.bd["ger_tar_bd"]
            print(f"Conexão realizada com sucesso!")
        except Exception as excecao:
            print(f"Não conectado ao Banco de dados!", excecao)
        

        # -------------------------------------------------------------
        # TÍTULO DA TAREFA
        # -------------------------------------------------------------

        ctk.CTkLabel(root, text="Título da Tarefa: ", font=("Arial bold", 15)).grid(row=0, column=0, columnspan=1, sticky="e",pady=15, padx=20)
        
        self.tit_tar = ctk.CTkEntry(root, width=445, border_width=1, border_color="#5e5e5e")
        self.tit_tar.grid(row=0, column=1, columnspan=1, pady=10)

        # -------------------------------------------------------------
        # DESCRIÇÃO DA TAREFA
        # -------------------------------------------------------------

        ctk.CTkLabel(root, text="Descrição da Tarefa: ", font=("Arial bold", 15)).grid(row=1, column=0, pady=10, sticky="n", columnspan=1, padx=20)

        self.desc_tar = ctk.CTkTextbox(root, width=445, height=100, border_width=1, border_color="#5e5e5e")
        self.desc_tar.grid(row=1, column=1, columnspan=1, pady=10)

        # -------------------------------------------------------------
        # FUNÇÕES dos botões
        # -------------------------------------------------------------

        def carregar_tarefas(status_filtro=None):
            # Limpa a tabela
            for item in self.tabela.get_children():
                self.tabela.delete(item)

            try:
                if status_filtro == "Todos" or status_filtro is None:
                    tarefas = listar_tarefas()
                else:
                    tarefas = listar_tarefas(status_filtro)

                for tar_id, titulo, descricao, status in tarefas:
                    self.tabela.insert(
                        "",
                        "end",
                        iid=str(tar_id),
                        values=(titulo, descricao, status)
                    )

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao carregar tarefas",
                    str(erro)
                )


        def aplicar_filtro():
            status = self.status_var.get()
            carregar_tarefas(status)


        def add_tar():
            titulo = self.tit_tar.get().strip()
            descricao = self.desc_tar.get("1.0", "end").strip()
            status = self.status_var.get()
            if status == "Todos":
                status = "Pendente"


            if not titulo or not descricao:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return
            
                    # Verifica se já existe tarefa com o mesmo título
            tarefa_existente = self.colecao.find_one({
                "titulo": titulo,
                "status": "Pendente"
            })


            if tarefa_existente:
                messagebox.showwarning(
                    "Tarefa já existente",
                    f"Já existe uma tarefa chamada '{titulo}'.\n"
                    "Conclua a tarefa existente antes de criar outra com o mesmo nome."
                )
                return
           
                        # Validação de tamanho
            if len(titulo) > 30:
                messagebox.showwarning(
                    "Título muito longo",
                    "O nome da tarefa deve ter no máximo 30 caracteres."
                )
                return

            if len(descricao) > 150:
                messagebox.showwarning(
                    "Descrição muito longa",
                    "A descrição pode conter até 150 caracteres."
                )
                return


            try:
                inserir_tarefa(titulo, descricao, status)

                self.tabela.insert(
                    "",
                    "end",
                    #iid=str(res.inserted_id),
                    values=(titulo, descricao, status)
                )

                messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

                # Limpar campos
                self.tit_tar.delete(0, "end")
                self.desc_tar.delete("1.0", "end")
                self.status_var.set("Pendente")

            except Exception as erro:
                messagebox.showerror("Erro", f"Erro ao inserir tarefa:\n{erro}")



        def up_tar():
            selecionado = self.tabela.selection()

            if not selecionado:
                messagebox.showwarning(
                    "Atenção",
                    "Selecione uma tarefa para atualizar."
                )
                return

            tarefa_id = selecionado[0]

            titulo = self.tit_tar.get().strip()
            descricao = self.desc_tar.get("1.0", "end").strip()
            status = self.status_var.get()
            if status == "Todos":
                status = "Pendente"


            if not titulo or not descricao:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            # Validação de tamanho
            if len(titulo) > 30:
                messagebox.showwarning(
                    "Título muito longo",
                    "O nome da tarefa deve ter no máximo 30 caracteres."
                )
                return

            if len(descricao) > 150:
                messagebox.showwarning(
                    "Descrição muito longa",
                    "A descrição pode conter até 150 caracteres."
                )
                return

            try:
                self.colecao.update_one(
                    {"_id": ObjectId(tarefa_id)},
                    {"$set": {
                        "titulo": titulo,
                        "descricao": descricao,
                        "status": status
                    }}
                )

                self.tabela.item(
                    tarefa_id,
                    values=(titulo, descricao, status)
                )

                messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")

                # Limpar campos e seleção
                self.tabela.selection_remove(tarefa_id)
                self.tit_tar.delete(0, "end")
                self.desc_tar.delete("1.0", "end")
                self.status_var.set("Pendente")

            except Exception as erro:
                messagebox.showerror("Erro", f"Erro ao atualizar tarefa:\n{erro}")

            

        def del_tar():       
            selecionado = self.tabela.selection()

            if not selecionado:
                messagebox.showwarning("Atenção", "Selecione uma tarefa para excluir.")
                return

            tarefa_id = selecionado[0]  # iid da linha (é o _id do MongoDB)

            confirmar = messagebox.askyesno(
                "Confirmar exclusão",
                "Tem certeza que deseja excluir esta tarefa?"
            )

            if not confirmar:
                return

            try:
                # Excluir do banco
                self.colecao.delete_one({"_id": ObjectId(tarefa_id)})

                # Excluir da tabela
                self.tabela.delete(tarefa_id)

                # Limpar campos após exclusão
                self.tit_tar.delete(0, "end")
                self.desc_tar.delete("1.0", "end")
                self.status_var.set("Pendente")
                self.tarefa_selecionada_id = None

                messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")

            except Exception as erro:
                messagebox.showerror("Erro", f"Erro ao excluir tarefa:\n{erro}")



        def selecionar_tarefa(event):
            selecionado = self.tabela.selection()

            if not selecionado:
                return

            tarefa_id = selecionado[0]
            self.tarefa_selecionada_id = tarefa_id
            valores = self.tabela.item(tarefa_id, "values")

            titulo, descricao, status = valores

            # Preencher campos
            self.tit_tar.delete(0, "end")
            self.tit_tar.insert(0, titulo)

            self.desc_tar.delete("1.0", "end")
            self.desc_tar.insert("1.0", descricao)

            self.status_var.set(status)

            
        # -------------------------------------------------------------
        # BOTÕES: Adicionar / Atualizar / Excluir
        # -------------------------------------------------------------

        btn = ctk.CTkFrame(root)
        btn.grid(row=2, column=1, pady=15, sticky="w", columnspan=2)

       
        self.btn_add = ctk.CTkButton(btn, text="Adicionar", text_color="#000000", command=add_tar)
        self.btn_add.grid(row=2, column=0, padx=5)

        btn_up = ctk.CTkButton(btn, text="Atualizar", text_color="#000000", command=up_tar)
        btn_up.grid(row=2, column=1, padx=5)

        btn_del = ctk.CTkButton(btn, text="Excluir", text_color="#000000", command=del_tar)
        btn_del.grid(row=2, column=2, padx=5)

        # -------------------------------------------------------------
        # STATUS (TAREFA + FUTURO FILTRO)
        # -------------------------------------------------------------

        ctk.CTkLabel(
            root,
            text="Status:",
            font=("Arial bold", 15)
        ).grid(row=3, column=0, sticky="e", padx=20, pady=15)

        self.status_var = ctk.StringVar(self.root, value="Pendente")

        self.status_menu = ctk.CTkOptionMenu(
            root,
            values=["Pendente", "Concluída", "Todos"],
            variable=self.status_var,
            width=150,
            text_color="#000000",
            dropdown_hover_color="#0870b1"
        )
        self.status_menu.grid(row=3, column=1, sticky="w")

        btn_flt = ctk.CTkButton(
            root,
            text="Aplicar Filtro",
            text_color="#000000",
            width=230,
            command=aplicar_filtro
        )
        btn_flt.grid(row=3, column=1, padx=30, sticky="e")

        
        # -------------------------------------------------------------
        # self.TABELA DE EXIBIÇÃO
        # -------------------------------------------------------------

        tarefas = []
        
        self.tabela = ttk.Treeview(self.root, columns=("Tìtulo", "Descrição", "Status"), show="headings")


        self.tabela.column("Tìtulo", minwidth=1, width=150)
        self.tabela.column("Descrição", minwidth=0, width=350)
        self.tabela.column("Status", minwidth=0, width=100)

        self.tabela.heading("Tìtulo", text="Tarefa")
        self.tabela.heading("Descrição", text="Descrição")
        self.tabela.heading("Status", text="Status")

        self.tabela.grid(row=4, column=1, columnspan=4)

        self.tabela.bind("<<TreeviewSelect>>", selecionar_tarefa)


        for (t, d, s) in tarefas:
            tarefas.insert("", "end", values=(t, d, s))

        
        carregar_tarefas("Todos")



# -------------------------------------------------------------
# INICIALIZAÇÃO DA JANELA
# -------------------------------------------------------------

root = ctk.CTk()

app = ger_tar_app (root)
root.mainloop()    


