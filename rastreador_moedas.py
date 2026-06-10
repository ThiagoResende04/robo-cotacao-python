import sqlite3
from datetime import datetime
import requests


def criar_banco():
    """Cria o banco de dados SQLite e a tabela se não existirem."""
    
    conexao = sqlite3.connect("cotacoes.db")
    cursor = conexao.cursor()

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_moedas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moeda TEXT NOT NULL,
            valor_reais REAL NOT NULL,
            data_consulta TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados e tabela preparados com sucesso!")


def buscar_cotacoes():
    """Acessa a API de economia para buscar o valor atual do Dólar e Euro."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"

    try:
        # Automação via requisição HTTP (sem precisar abrir o navegador)
        resposta = requests.get(url)
        dados = resposta.json()

        
        preco_dolar = float(dados["USDBRL"]["bid"])
        preco_euro = float(dados["EURBRL"]["bid"])

        return {"USD": preco_dolar, "EUR": preco_euro}

    except Exception as e:
        print(f"Erro ao buscar cotações: {e}")
        return None


def salvar_no_banco(dados_cotacao):
    """Salva as cotações extraídas dentro do banco de dados SQL."""
    if not dados_cotacao:
        return

    conexao = sqlite3.connect("cotacoes.db")
    cursor = conexao.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    for moeda, valor in dados_cotacao.items():
        cursor.execute(
            """
            INSERT INTO historico_moedas (moeda, valor_reais, data_consulta)
            VALUES (?, ?, ?)
        """,
            (moeda, valor, data_atual),
        )

        print(f"Salvo no banco: {moeda} - R$ {valor:.2f} em {data_atual}")

    conexao.commit()
    conexao.close()



if __name__ == "__main__":
    print("Iniciando o script de automação...")
    criar_banco()
    cotacoes_atuais = buscar_cotacoes()
    salvar_no_banco(cotacoes_atuais)
    print("Processo finalizado com sucesso!")
