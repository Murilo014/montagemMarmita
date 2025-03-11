from flask import Flask, render_template, request, redirect, url_for
from consultaSql import cadastro_refeicao, listar_refeicao, obter_porcoes, atualizar_refeicao, obter_refeicao

app = Flask(__name__)

@app.route("/marmitas")
def marmitas():
    refeicoes = listar_refeicao()
    return render_template("marmitas.html", refeicoes=refeicoes)

@app.route("/cadastroRefeicao", methods=["GET", "POST"])
def cadastro_marmitas():
    if request.method == "POST":
        # Obter dados do formulário
        numero_dia = request.form.get("dia")  # Recebe o número do dia
        nome_refeicao = request.form.get("nome_refeicao")
        ingredientes = request.form.get("ingredientes")
        porcoes = request.form.getlist("porcoes")

        # Mapear o número para o nome do dia
        dias_da_semana = {
            "1": "Segunda-feira",
            "2": "Terça-feira",
            "3": "Quarta-feira",
            "4": "Quinta-feira",
            "5": "Sexta-feira",
            "6": "Sábado",
            "7": "Domingo"
        }
        dia = dias_da_semana.get(numero_dia, "Dia inválido")

        # Verifica se pelo menos uma porção foi selecionada
        if not porcoes:
            return "Erro: Selecione pelo menos um tipo de porção (Almoço ou Janta)."

        # Inserir no banco de dados
        sucesso = cadastro_refeicao(dia, nome_refeicao, ingredientes, porcoes)
        if sucesso:
            return redirect(url_for("marmitas"))  # Redireciona para a página de listagem
        else:
            return "Erro ao cadastrar refeição."

    # Se for GET, carregar a página de cadastro
    dias_da_semana = [
        ("1", "Segunda-feira"),
        ("2", "Terça-feira"),
        ("3", "Quarta-feira"),
        ("4", "Quinta-feira"),
        ("5", "Sexta-feira"),
        ("6", "Sábado"),
        ("7", "Domingo")
    ]

    porcoes = [("1", "Almoço"), ("2", "Janta")]
    return render_template("cadastroRefeicao.html", dias_da_semana=dias_da_semana, porcoes=porcoes)

@app.route("/editaMarmita/<int:id_refeicao>", methods=["GET", "POST"])
def edita_marmitas(id_refeicao):
    if request.method == "POST":
        numero_dia = request.form.get("dia")
        nome_refeicao = request.form.get("nome_refeicao")
        ingredientes = request.form.get("ingredientes")
        porcoes = request.form.getlist("porcoes")

        # Mapeamento dos dias da semana
        dias_da_semana = {
            "1": "Segunda-feira",
            "2": "Terça-feira",
            "3": "Quarta-feira",
            "4": "Quinta-feira",
            "5": "Sexta-feira",
            "6": "Sábado",
            "7": "Domingo"
        }
        dia = dias_da_semana.get(numero_dia, "Dia inválido")

        # Normalizar porções
        porcoes = [int(p) for p in porcoes if p.isdigit()]

        sucesso = atualizar_refeicao(id_refeicao, dia, nome_refeicao, ingredientes, porcoes)
        if sucesso:
            return redirect(url_for("marmitas"))  # 🔹 Agora redireciona corretamente
        else:
            return "Erro ao atualizar refeição."

    # 🔹 Buscar refeição e tratar caso não exista
    refeicao, porcoes_selecionadas = obter_refeicao(id_refeicao)

    if refeicao is None:
        return "Refeição não encontrada", 404  # Evita erro no template

    dias_da_semana = [
        ("1", "Segunda-feira"),
        ("2", "Terça-feira"),
        ("3", "Quarta-feira"),
        ("4", "Quinta-feira"),
        ("5", "Sexta-feira"),
        ("6", "Sábado"),
        ("7", "Domingo")
    ]
    
    # Buscar todas as porções disponíveis
    porcoes = obter_porcoes()

    return render_template(
        "editaMarmita.html",
        refeicao=refeicao,
        porcoes=porcoes,
        porcoes_selecionadas=porcoes_selecionadas
    )



if __name__ == "__main__":
    app.run(debug=True)