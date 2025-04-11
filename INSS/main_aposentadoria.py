from datetime import datetime

import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors
from flet.core.border_radius import horizontal
from flet.core.colors import Colors
from flet.core.dropdown import Option
from flet.core.types import MainAxisAlignment, CrossAxisAlignment


def main(page: ft.Page):
    page.title = "INSS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667

    def tela(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    ft.Image(src='INSS.svg.png'),
                    ElevatedButton(text="Simulção de aposentadoria", on_click=lambda _: page.go("/simulacao")),
                    ElevatedButton(text="Ver regras", on_click=lambda _: page.go("/regras")),
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/simulacao":
            page.views.append(
                View(
                    "/simulacao",
                    [
                        AppBar(title=Text("Simulação INSS"), bgcolor=Colors.SECONDARY_CONTAINER),
                        Text("Requisitos Básicos do Sistema"),
                        Text(" Entradas do Usuário:\n\n"),
                        input_idade,
                        genero,
                        input_tempo_contribuicao,
                        input_media_salarial,
                        categoria,
                        ElevatedButton(text="Resultado", on_click=lambda _: aposentadoria_simulacao(e)),
                    ], vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/resultado":
            page.views.clear()
            page.views.append(
                View(
                    "/",
                    [
                        AppBar(title=Text("Resultado"), bgcolor=Colors.SECONDARY_CONTAINER),
                        Text(" Resultado final\n\n"),
                        text_resultado,
                        ElevatedButton(text="Voltar", on_click=lambda _: page.go("/aposentadoria_simulacao")),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/regras":
            page.views.append(
                View(
                    "/regras",
                    [
                        AppBar(title=Text("Regras do INSS"), bgcolor=Colors.SECONDARY_CONTAINER),
                        Text("Regras Básicas de Aposentadoria:\n\n"),

                        Text(
                            "Aposentadoria por Idade:\n\n"
                            "Homens: 65 anos de idade e pelo menos 15 anos de contribuição.\n "
                            "Mulheres: 62 anos de idade e pelo menos 15 anos de contribuição.\n\n"),
                        Text(
                            "Aposentadoria por Tempo de Contribuição:\n\n "
                            "Homens: 35 anos de contribuição.\n"
                            "Mulheres: 30 anos de contribuição.\n\n"),
                        Text(
                            "Valor Estimado do Benefício:\n\n"
                            " O valor da aposentadoria será uma média de 60% da média salarial informada, acrescido de 2% por ano que exceder o tempo mínimo de contribuição.")
                    ]
                )
            )

        page.update()

    def aposentadoria_simulacao(e):
        try:
            if not input_media_salarial.value:
                input_media_salarial.error = True
                input_media_salarial.error_text = "Preencha todos os campos"
                page.update()

            if not input_tempo_contribuicao.value:
                input_tempo_contribuicao.error = True
                input_tempo_contribuicao.error_text = "Preencha todos os campos"
                page.update()

            if not input_idade.value:
                input_idade.error = True
                input_idade.error_text = "Preencha todos os campos"
                page.update()

            if genero.value:
                genero.error = True
                genero.error_text = "Preencha todos  os campos"
                page.update()

            if categoria.value:
                categoria.error = True
                categoria.error_text = "Preencha todos os campos"
                page.update()

            pergunta = int(input_idade.value)
            contribuicao = int(input_tempo_contribuicao.value)
            Masc = genero
            Fem = genero
            resultado = salario(e)

            if categoria.value == "idd":
                if genero == Fem:
                    if pergunta < 62 or pergunta > 120 and contribuicao < 15:
                        text_resultado.value = " Não tem direito ao INSS"
                        text_resultado.value = f"O valor estimado é R${resultado}"

                    elif pergunta >= 62 or pergunta <= 120 and contribuicao >= 15:
                        text_resultado.value = "Tem direito ao INSS"
                        text_resultado.value = f"O valor estimado é R$ {resultado}"

                elif genero == Masc:
                    if pergunta < 65 or pergunta > 120 and contribuicao < 15:
                        text_resultado.value = "Não tem direito ao INSS"
                        text_resultado.value = f"O valor estimado é R$ {resultado}"

                    elif pergunta >= 65 or pergunta < 120 and contribuicao >= 15:
                        text_resultado.value = " Tem direiro ao INSS"
                        text_resultado.value = f"O valor estimado é R$ {resultado}"

            elif categoria.value == "Contri":
                if genero == Masc:
                    if contribuicao < 35 or contribuicao > 80:
                        text_resultado.value = "Não tem direito ao INSS"
                        text_resultado.value = f"O valor estimado é R${resultado}"

                elif genero == Masc:
                    if contribuicao >= 35 or contribuicao <= 80:
                        text_resultado.value = "Tem direito ao INSS"
                        text_resultado.value = f"O valor estimado é R${resultado}"

            page.update()
            page.go("/resultado")
        except ValueError:
            text_resultado.value = "Digite apenas números!"

    def salario(e,):
        try:
            contribuicao_valor = float(input_tempo_contribuicao.value)
            salario = float(input_media_salarial.value)
            media = (salario * 60/100)
            print(media)

            if contribuicao_valor > 15:
                diferenca = (contribuicao_valor - 15) * 2
                acrescentado = (salario  * diferenca) / 100
                resultado = (media + acrescentado)
                return resultado
            else:
                return media

        except Exception as e:
            text_resultado.value = "Digite apenas números!"

    input_idade = ft.TextField(label="Idade: ", hint_text="Digite sua idade")
    input_tempo_contribuicao = ft.TextField(label="Tempo de contribuição com o INSS até o momento",hint_text="Número de anos de contribuição")
    input_media_salarial = ft.TextField(label="Digite a média salarial dos últimos anos ",hint_text="Pelo menos dos últimos 5 anos de contribuição")
    genero = ft.Dropdown(
        label="Genero",
        width=page.window.width,
        fill_color=Colors.PURPLE,
        options=[Option(key='Masc', text='Masculino'), Option(key='Fem', text='Feminino')],
    )

    categoria = ft.Dropdown(
        label="Categoria",
        width=page.window.width,
        fill_color=Colors.PURPLE,
        options=[Option(key='Contri', text='Contribuição'), Option(key='idd', text='Idade')],
    )

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    text_resultado = ft.Text(value="")
    page.on_route_change = tela
    page.on_view_pop = voltar

    page.go(page.route)


ft.app(main)
