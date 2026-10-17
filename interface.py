
import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar
from auth import verificar_senha
from dados import tipos_combustivel


class PostoMatos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Posto Matos - Gerenciamento")
        self.janela.geometry("950x600")
        self.janela.minsize(800, 500)

        self.registro_id = None

        self.montar_interface()
        self.carregar_registros()

    def montar_interface(self):
        principal = ttk.Frame(self.janela, padding=12)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="POSTO MATOS",
            font=("Arial", 18, "bold")
        ).pack(pady=5)

        formulario = ttk.LabelFrame(
            principal, text="Dados do abastecimento", padding=10
        )
        formulario.pack(fill="x", pady=8)

        ttk.Label(formulario, text="Nome do cliente").grid(
            row=0, column=0, sticky="w", padx=5, pady=4
        )
        self.nome = ttk.Entry(formulario, width=28)
        self.nome.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="CPF").grid(
            row=0, column=2, sticky="w", padx=5, pady=4
        )
        self.cpf = ttk.Entry(formulario, width=18)
        self.cpf.grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(formulario, text="Combustível").grid(
            row=1, column=0, sticky="w", padx=5, pady=4
        )
        self.combustivel = ttk.Combobox(
            formulario,
            values=tipos_combustivel,
            state="readonly",
            width=25
        )
        self.combustivel.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="Litros").grid(
            row=1, column=2, sticky="w", padx=5, pady=4
        )
        self.litros = ttk.Entry(formulario, width=18)
        self.litros.grid(row=1, column=3, padx=5, pady=4)

        ttk.Label(formulario, text="Preço por litro (R$)").grid(
            row=2, column=0, sticky="w", padx=5, pady=4
        )
        self.preco = ttk.Entry(formulario, width=18)
        self.preco.grid(row=2, column=1, padx=5, pady=4)

        botoes = ttk.Frame(principal)
        botoes.pack(fill="x", pady=5)

        ttk.Button(
            botoes, text="Cadastrar", command=self.cadastrar
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Editar", command=self.editar
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Excluir", command=self.excluir
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Limpar", command=self.limpar
        ).pack(side="left", padx=3)

        pesquisa = ttk.LabelFrame(
            principal, text="Pesquisar por ID, CPF ou nome", padding=8
        )
        pesquisa.pack(fill="x", pady=5)

        self.busca = ttk.Entry(pesquisa, width=35)
        self.busca.pack(side="left", padx=5)

        ttk.Button(
            pesquisa, text="Pesquisar", command=self.pesquisar
        ).pack(side="left", padx=3)

        ttk.Button(
            pesquisa, text="Mostrar todos",
            command=self.carregar_registros
        ).pack(side="left", padx=3)

        colunas = (
            "id", "nome", "cpf", "combustivel",
            "litros", "preco", "total"
        )

        self.tabela = ttk.Treeview(
            principal, columns=colunas, show="headings", height=12
        )

        titulos = {
            "id": "ID",
            "nome": "Cliente",
            "cpf": "CPF",
            "combustivel": "Combustível",
            "litros": "Litros",
            "preco": "Preço/Litro",
            "total": "Valor Total"
        }

        larguras = {
            "id": 45, "nome": 150, "cpf": 120,
            "combustivel": 145, "litros": 75,
            "preco": 100, "total": 100
        }

        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(
                coluna, width=larguras[coluna], anchor="center"
            )

        self.tabela.pack(fill="both", expand=True, pady=8)
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar)

    def executar(self, funcao):
        try:
            funcao()
        except Exception as erro:
            messagebox.showerror(
                "Erro", f"Não foi possível concluir a operação.\n\n{erro}"
            )

    def carregar_registros(self, filtro=None):
        def operacao():
            with conectar() as conn:
                with conn.cursor() as cursor:
                    sql = """
                        SELECT a.id, c.nome, c.cpf, a.combustivel,
                               a.litros, a.preco_litro, a.valor_total
                        FROM abastecimentos a
                        JOIN clientes c ON c.id = a.cliente_id
                    """
                    parametros = ()

                    if filtro:
                        if filtro.isdigit():
                            sql += " WHERE a.id = %s"
                            parametros = (int(filtro),)
                        else:
                            sql += """
                                WHERE c.cpf = %s
                                   OR c.nome ILIKE %s
                            """
                            parametros = (filtro, f"%{filtro}%")

                    sql += " ORDER BY a.id"

                    cursor.execute(sql, parametros)
                    registros = cursor.fetchall()

            self.tabela.delete(*self.tabela.get_children())

            for registro in registros:
                self.tabela.insert("", "end", values=registro)

            self.registro_id = None

        self.executar(operacao)

    def pesquisar(self):
        filtro = self.busca.get().strip()

        if not filtro:
            messagebox.showwarning(
                "Atenção", "Digite um ID, CPF ou nome para pesquisar."
            )
            return

        self.carregar_registros(filtro)

        registros = self.tabela.get_children()
        if registros:
            self.tabela.selection_set(registros[0])
            self.tabela.focus(registros[0])
            self.tabela.see(registros[0])
        else:
            messagebox.showinfo("Pesquisa", "Nenhum abastecimento encontrado.")

    def selecionar(self, evento=None):
        selecionados = self.tabela.selection()

        if not selecionados:
            return

        valores = self.tabela.item(selecionados[0], "values")
        if not valores:
            return

        self.registro_id = int(valores[0])

        self.limpar_campos()

        self.nome.insert(0, valores[1])
        self.cpf.insert(0, valores[2])
        self.combustivel.set(valores[3])
        self.litros.insert(0, str(valores[4]))
        self.preco.insert(0, str(valores[5]))

    def obter_dados(self):
        nome = self.nome.get().strip()
        cpf = "".join(c for c in self.cpf.get() if c.isdigit())
        combustivel = self.combustivel.get()
        litros_texto = self.litros.get().strip().replace(",", ".")
        preco_texto = self.preco.get().strip().replace(",", ".")

        if not nome or not cpf or not combustivel:
            raise ValueError("Preencha nome, CPF e combustível.")

        if len(cpf) != 11:
            raise ValueError("O CPF deve conter 11 números.")

        if combustivel not in tipos_combustivel:
            raise ValueError("Selecione um combustível válido.")

        try:
            litros = float(litros_texto)
            preco = float(preco_texto)
        except ValueError:
            raise ValueError("Informe litros e preço usando números válidos.")

        if litros <= 0 or preco <= 0:
            raise ValueError("Litros e preço devem ser maiores que zero.")

        return nome, cpf, combustivel, litros, preco

    def cadastrar(self):
        def operacao():
            nome, cpf, combustivel, litros, preco = self.obter_dados()
            total = round(litros * preco, 2)

            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM clientes WHERE cpf = %s",
                        (cpf,)
                    )
                    cliente = cursor.fetchone()

                    if cliente:
                        cliente_id = cliente[0]
                        cursor.execute(
                            "UPDATE clientes SET nome = %s WHERE id = %s",
                            (nome, cliente_id)
                        )
                    else:
                        cursor.execute(
                            """
                            INSERT INTO clientes (nome, cpf)
                            VALUES (%s, %s)
                            RETURNING id
                            """,
                            (nome, cpf)
                        )
                        cliente_id = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO abastecimentos
                            (cliente_id, combustivel, litros,
                             preco_litro, valor_total)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (cliente_id, combustivel, litros, preco, total)
                    )

            messagebox.showinfo(
                "Sucesso", "Abastecimento cadastrado!"
            )
            self.limpar()
            self.carregar_registros()

        self.executar(operacao)

    def editar(self):
        if not self.registro_id:
            messagebox.showwarning(
                "Atenção",
                "Selecione um abastecimento na tabela antes de editar."
            )
            return

        def operacao():
            nome, cpf, combustivel, litros, preco = self.obter_dados()
            total = round(litros * preco, 2)
            registro_id = self.registro_id

            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT cliente_id FROM abastecimentos
                        WHERE id = %s
                        """,
                        (registro_id,)
                    )
                    registro = cursor.fetchone()

                    if not registro:
                        raise ValueError("O abastecimento não foi encontrado.")

                    cliente_id = registro[0]

                    cursor.execute(
                        """
                        SELECT id FROM clientes
                        WHERE cpf = %s AND id <> %s
                        """,
                        (cpf, cliente_id)
                    )

                    if cursor.fetchone():
                        raise ValueError(
                            "Esse CPF pertence a outro cliente. "
                            "Confira o CPF informado."
                        )

                    cursor.execute(
                        """
                        UPDATE clientes
                        SET nome = %s, cpf = %s
                        WHERE id = %s
                        """,
                        (nome, cpf, cliente_id)
                    )

                    cursor.execute(
                        """
                        UPDATE abastecimentos
                        SET combustivel = %s, litros = %s,
                            preco_litro = %s, valor_total = %s
                        WHERE id = %s
                        """,
                        (
                            combustivel, litros, preco,
                            total, registro_id
                        )
                    )

            messagebox.showinfo("Sucesso", "Abastecimento atualizado!")
            self.limpar()
            self.carregar_registros()

        self.executar(operacao)

    def excluir(self):
        if not self.registro_id:
            messagebox.showwarning(
                "Atenção", "Selecione um abastecimento na tabela."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o abastecimento ID {self.registro_id}?"
        )

        if not confirmar:
            return

        def operacao():
            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM abastecimentos WHERE id = %s",
                        (self.registro_id,)
                    )

            messagebox.showinfo("Sucesso", "Abastecimento excluído!")
            self.limpar()
            self.carregar_registros()

        self.executar(operacao)

    def limpar_campos(self):
        self.nome.delete(0, tk.END)
        self.cpf.delete(0, tk.END)
        self.combustivel.set("")
        self.litros.delete(0, tk.END)
        self.preco.delete(0, tk.END)

    def limpar(self):
        self.registro_id = None
        self.limpar_campos()
        for item in self.tabela.selection():
            self.tabela.selection_remove(item)


def abrir_sistema():
    janela = tk.Tk()
    PostoMatos(janela)
    janela.mainloop()


def realizar_login():
    login = tk.Tk()
    login.title("Login - Posto Matos")
    login.geometry("350x230")
    login.resizable(False, False)

    quadro = ttk.Frame(login, padding=20)
    quadro.pack(fill="both", expand=True)

    ttk.Label(
        quadro, text="POSTO MATOS", font=("Arial", 16, "bold")
    ).pack(pady=8)

    ttk.Label(quadro, text="Usuário").pack(anchor="w")
    campo_usuario = ttk.Entry(quadro)
    campo_usuario.pack(fill="x", pady=4)

    ttk.Label(quadro, text="Senha").pack(anchor="w")
    campo_senha = ttk.Entry(quadro, show="*")
    campo_senha.pack(fill="x", pady=4)

    def entrar(event=None):
        usuario = campo_usuario.get().strip()
        senha = campo_senha.get()

        if not usuario or not senha:
            messagebox.showwarning(
                "Atenção", "Digite o usuário e a senha.", parent=login
            )
            return

        try:
            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT senha_hash FROM usuarios WHERE usuario = %s",
                        (usuario,)
                    )
                    registro = cursor.fetchone()

            if registro and verificar_senha(senha, registro[0]):
                login.destroy()
                abrir_sistema()
            else:
                messagebox.showerror(
                    "Login", "Usuário ou senha incorretos.", parent=login
                )
                campo_senha.delete(0, tk.END)

        except Exception as erro:
            messagebox.showerror(
                "Erro de conexão",
                f"Não foi possível acessar o banco de dados.\n\n{erro}",
                parent=login
            )

    ttk.Button(
        quadro, text="Entrar", command=entrar
    ).pack(fill="x", pady=10)

    campo_senha.bind("<Return>", entrar)
    campo_usuario.focus_set()
    login.mainloop()


if __name__ == "__main__":
    realizar_login()
