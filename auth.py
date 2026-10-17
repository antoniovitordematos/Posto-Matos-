
import hashlib
import hmac
import secrets

from conexao import conectar


def gerar_hash(senha):
    salt = secrets.token_bytes(16)

    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        600000
    )

    return (
        f"pbkdf2_sha256$600000$"
        f"{salt.hex()}${resultado.hex()}"
    )


def verificar_senha(senha, senha_hash):
    try:
        algoritmo, iteracoes, salt_hex, hash_hex = senha_hash.split("$")

        if algoritmo != "pbkdf2_sha256":
            return False

        resultado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iteracoes)
        )

        return hmac.compare_digest(resultado.hex(), hash_hex)

    except (ValueError, TypeError):
        return False


def existe_usuario():
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM usuarios)"
            )
            return cursor.fetchone()[0]


def cadastrar_usuario_inicial():
    print("\n--- CADASTRO DO PRIMEIRO USUÁRIO ---")

    nome = input("Nome: ").strip()
    usuario = input("Crie um nome de usuário: ").strip()

    if not nome or not usuario:
        print("Nome e usuário são obrigatórios.")
        return False

    senha = input("Crie uma senha: ")
    confirmacao = input("Digite a senha novamente: ")

    if len(senha) < 8:
        print("A senha deve ter pelo menos 8 caracteres.")
        return False

    if senha != confirmacao:
        print("As senhas não conferem.")
        return False

    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, usuario, senha_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (nome, usuario, gerar_hash(senha))
                )

        print("Usuário cadastrado com sucesso!")
        return True

    except Exception:
        print(
            "Não foi possível cadastrar o usuário. "
            "Verifique se o nome de usuário já existe."
        )
        return False


def autenticar():
    while True:
        if not existe_usuario():
            print("\nNenhum usuário cadastrado.")

            if not cadastrar_usuario_inicial():
                tentar = input(
                    "Tentar novamente? (s/n): "
                ).strip().lower()

                if tentar != "s":
                    return False

                continue

        break

    for tentativa in range(3):
        print("\n--- LOGIN — POSTO MATOS ---")

        usuario = input("Usuário: ").strip()
        senha = input("Senha: ")

        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT senha_hash
                    FROM usuarios
                    WHERE usuario = %s
                    """,
                    (usuario,)
                )
                registro = cursor.fetchone()

        if registro and verificar_senha(senha, registro[0]):
            print("\nLogin realizado com sucesso!")
            return True

        print("Usuário ou senha incorretos.")

    print("Número de tentativas excedido.")
    return False
