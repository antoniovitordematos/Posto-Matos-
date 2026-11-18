
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from conexao import conectar


def consultar_dashboard():
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(valor_total), 0),
                       COALESCE(MAX(valor_total), 0),
                       COALESCE(MIN(valor_total), 0)
                FROM abastecimentos
            """)
            indicadores = cursor.fetchone()

            cursor.execute("""
                SELECT combustivel, COUNT(*) AS quantidade,
                       SUM(valor_total) AS faturamento
                FROM abastecimentos
                GROUP BY combustivel
                ORDER BY faturamento DESC
            """)
            combustiveis = cursor.fetchall()

    return indicadores, combustiveis


def formatar_moeda(valor):
    numero = f"{float(valor):,.2f}"
    return "R$ " + numero.replace(",", "X").replace(".", ",").replace("X", ".")


def abrir_dashboard(janela_pai):
    janela = tk.Toplevel(janela_pai)
    janela.title("Posto Matos - Dashboard")
    janela.geometry("1100x700")
    janela.minsize(850, 550)
    janela.configure(bg="#f3f5f9")

    titulo = tk.Label(
        janela,
        text="DASHBOARD - POSTO MATOS",
        font=("Arial", 20, "bold"),
        bg="#f3f5f9",
        fg="#1e293b"
    )
    titulo.pack(pady=20)

    painel = tk.Frame(janela, bg="#f3f5f9")
    painel.pack(fill="x", padx=20, pady=10)

    nomes = [
        "Total de abastecimentos",
        "Faturamento total",
        "Maior abastecimento",
        "Menor abastecimento"
    ]

    valores_labels = []

    for i, nome in enumerate(nomes):
        painel.grid_columnconfigure(i, weight=1)

        cartao = tk.Frame(
            painel,
            bg="white",
            padx=12,
            pady=20,
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )
        cartao.grid(row=0, column=i, sticky="nsew", padx=5)

        tk.Label(
            cartao,
            text=nome,
            font=("Arial", 10),
            bg="white",
            fg="#64748b"
        ).pack()

        valor_label = tk.Label(
            cartao,
            text="--",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#1e293b"
        )
        valor_label.pack(pady=10)
        valores_labels.append(valor_label)

    area_graficos = tk.Frame(janela, bg="white")
    area_graficos.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    figura = Figure(figsize=(10, 4), dpi=100)
    canvas = FigureCanvasTkAgg(figura, master=area_graficos)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_dashboard():
        try:
            indicadores, combustiveis = consultar_dashboard()
        except Exception as erro:
            messagebox.showerror(
                "Erro no Dashboard",
                f"Não foi possível consultar o banco:\n{erro}",
                parent=janela
            )
            return

        total, faturamento, maior, menor = indicadores

        valores_labels[0].config(text=str(total))
        valores_labels[1].config(text=formatar_moeda(faturamento))
        valores_labels[2].config(text=formatar_moeda(maior))
        valores_labels[3].config(text=formatar_moeda(menor))

        figura.clear()

        grafico_barras = figura.add_subplot(121)
        grafico_pizza = figura.add_subplot(122)

        if combustiveis:
            nomes_combustiveis = [r[0] for r in combustiveis]
            quantidades = [r[1] for r in combustiveis]
            faturamentos = [float(r[2]) for r in combustiveis]

            grafico_barras.barh(
                nomes_combustiveis,
                faturamentos,
                color="#2563eb"
            )
            grafico_barras.invert_yaxis()
            grafico_barras.set_title("Faturamento por combustível")
            grafico_barras.set_xlabel("Valor em R$")

            grafico_pizza.pie(
                quantidades,
                labels=nomes_combustiveis,
                autopct="%1.1f%%",
                startangle=90
            )
            grafico_pizza.set_title("Abastecimentos por combustível")
        else:
            grafico_barras.text(
                0.5, 0.5, "Sem dados",
                ha="center", va="center"
            )
            grafico_pizza.text(
                0.5, 0.5, "Sem dados",
                ha="center", va="center"
            )

        figura.tight_layout(pad=3)
        canvas.draw()

    tk.Button(
        janela,
        text="Atualizar Dashboard",
        command=atualizar_dashboard,
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        padx=20,
        pady=10,
        cursor="hand2"
    ).pack(pady=15)

    atualizar_dashboard()
