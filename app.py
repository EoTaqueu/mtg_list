from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

def ler_csv():
    dados = []
    caminho_csv = os.path.join(os.path.dirname(__file__), 'mtglista.csv')
    with open(caminho_csv, newline='', encoding='utf-8') as arquivo_csv:
        leitor = csv.DictReader(arquivo_csv, delimiter=';')
        for linha in leitor:
            dados.append(linha)
    return dados

@app.route('/')
def mostrar_tabela():
    # Obtém os dados do CSV
    dados = ler_csv()

    # Obtém os parâmetros da URL
    sort_by = request.args.get('sort_by', default='nome')  # Coluna para ordenar
    order = request.args.get('order', default='asc')  # 'asc' ou 'desc'

    # Define se a ordenação será invertida
    reverse = (order == 'desc')

    # Ordena os dados
    try:
        if sort_by == 'valor':
            # Converte valores para float antes de ordenar
            dados_ordenados = sorted(dados, key=lambda x: float(x[sort_by].replace('R$ ', '')), reverse=reverse)
        else:
            # Ordena como string normal
            dados_ordenados = sorted(dados, key=lambda x: x[sort_by], reverse=reverse)
    except KeyError:
        # Se a coluna não existir, mantém a ordem original
        dados_ordenados = dados

    return render_template('index.html', dados=dados_ordenados, sort_by=sort_by, order=order)


if __name__ == '__main__':
    app.run(debug=True)





