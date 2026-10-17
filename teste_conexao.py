
from conexao import conectar

try:
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            resultado = cursor.fetchone()
            print("Conexão realizada com sucesso!")
            print(resultado[0])
except Exception as erro:
    print("Erro ao conectar:", erro)
