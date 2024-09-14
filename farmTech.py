import math
import numpy as np
import pandas as pd
from tabulate import tabulate
from terrainDetail import Terrain

# Nome das colunas
CODIGO_PRODUTO = "Codigo_Produto"
LARGURA = "Largura"
COMPRIMENTO = "Comprimento"
AREA_TOTAL = "Area_Total"
AREA_UTIL = "Area_Util"
NUMERO_LINHAS = "Numero_Linhas"
NUMERO_RUAS = "Numero_Ruas"
QUANTIDADE_ADUBO_NITROGENADO = "Quantidade_Adubo_Nitrogenado"
QUANTIDADE_SEMENTES = "Quantidade_Sementes"

# Cabeçalho
header = [
    CODIGO_PRODUTO,
    LARGURA,
    COMPRIMENTO,
    AREA_TOTAL,
    AREA_UTIL,
    NUMERO_LINHAS,
    NUMERO_RUAS,
    QUANTIDADE_ADUBO_NITROGENADO,
    QUANTIDADE_SEMENTES,
]

# Lê o csv e define que o separador é um ponto e vírgula
df = pd.read_csv('informacoes_culturas.csv', sep=';')

# Função para exibir o menu de seleção de funções
def menuSelection():
    while True:
        try:
            print('|-------------------------------------------------------------------|')
            print('| Olá, seja bem vindo ao seu aplicativo de gerenciamento de terrenos|')
            print('| Escolha a opção que deseja fazer.                                 |')
            print('|1 - Ver todos os terrenos                                          |')
            print('|2 - Inserir mais um terreno                                        |')
            print('|3 - Editar um terreno                                              |')
            print('|4 - Remover um terreno                                             |')
            print('|5 - Sair do programa                                               |')
            print('|-------------------------------------------------------------------|')
            data = int(input("Escolha a opção: "))
            break
        except:
            print('ERRO: Apenas números inteiros são válidos.\n')
    return data

# Função para perguntar ao usuário dados sobre as dimensões do terreno
def getTerrainData(culture):
    while True:
        try:
            width = float(input("Digite a largura do terreno (em metros): ").replace(',','.')) # Caso usuário use um numero de ponto flutuante com vírgula, converte para ponto
            length = float(input("Digite o comprimento do terreno (em metros): ").replace(',','.'))
            space_line = float(input("Digite o espaçamento entre linhas (em metros): ").replace(',','.'))
            width_street = float(input("Digite a largura das ruas (em metros): ").replace(',','.'))
            break
        except:
            print("ERRO: Apenas números reais são válidos.\n")
            input("Aperte Enter para reiniciar")
    
    return Terrain(culture, width, length, space_line, width_street)

# Função para retornar todos os dados do CSV
def get():
    print(tabulate(df, headers= header))
    input("Aperte enter para voltar ao menu")

# Função para inserir uma linha no DataFrame
def insert():
    terrainData = calculateDataCulture()
    new_line = pd.DataFrame({
        CODIGO_PRODUTO: [terrainData.product_code],
        LARGURA: [terrainData.width],
        COMPRIMENTO: [terrainData.length],
        AREA_TOTAL: [terrainData.total_area],
        AREA_UTIL: [terrainData.usable_area],
        NUMERO_LINHAS: [terrainData.line_number],
        NUMERO_RUAS: [terrainData.street_number],
        QUANTIDADE_ADUBO_NITROGENADO: [terrainData.nitrogen_fertilizer],
        QUANTIDADE_SEMENTES: [terrainData.quantity_seeds],
    })

    # Variavel global para modificar o dataframe para toda a aplicação
    global df
    df = pd.concat([df, new_line], ignore_index=True)
    input("Aperte enter para voltar ao menu")

# Função para edição de uma linha especifica do Dataframe
def edit():
    while True:
        try:
            index = int(input('Escolha o índice que deseja editar: '))
            break
        except:
            print('Índice inválido.')

    terrainData = calculateDataCulture()
    edit_line = {
        CODIGO_PRODUTO: terrainData.product_code,
        LARGURA: terrainData.width,
        COMPRIMENTO: terrainData.length,
        AREA_TOTAL: terrainData.total_area,
        AREA_UTIL: terrainData.usable_area,
        NUMERO_LINHAS: terrainData.line_number,
        NUMERO_RUAS: terrainData.street_number,
        QUANTIDADE_ADUBO_NITROGENADO: terrainData.nitrogen_fertilizer,
        QUANTIDADE_SEMENTES: terrainData.quantity_seeds,
    }

    global df
    df.loc[index] = edit_line
    input("Aperte enter para voltar ao menu")

# Função para deletar uma linha específica do Dataframe
def delete():
    global df
    while True:
        try:
            index = int(input('Escolha o índice que deseja remover: '))
            if index > df.shape[0] -1:
                print('Não existe este índice no banco de dados')
                continue
            break
        except:
            print('Índice inválido.')

    df = df.drop(index)
    input("Aperte enter para voltar ao menu")

# Função para escolher a cultura e em seguida realizar os cálculos de insumos para tal cultura
def calculateDataCulture():
    while True:
        try:
            print('| Escolha a cultura que será cultivada no terreno.                  |')
            print('|1 - Café                                                           |')
            print('|2 - Soja                                                           |')
            culture = int(input("Escolha a opção: "))
        except:
            input("Cultura inválida, aperte ENTER e tente novamente.")
            continue

        match culture:
            case 1:
                fertilizer_dose = 100  # kg/ha 
                seed_purity = 0.98
                planting_density = 300000  # plantas/ha
                seed_weight = 0.05 / 1000  # Peso médio da semente de café em kg (0.05 gramas por semente)
                break
            case 2:
                fertilizer_dose = 80  # kg/ha
                seed_purity = 0.95
                planting_density = 500000  # plantas/ha
                seed_weight = 0.2 / 1000  # Peso médio da semente de café em kg (0.05 gramas por semente)
                break
            case _:
                print("Opção inválida, tente novamente.\n")
        
    terrainData = getTerrainData(culture)
    total_area, usable_area, line_number, street_number = calculateTerrain(terrainData.width, terrainData.length, terrainData.space_line, terrainData.street_width)

    nitrogen_fertilizer = (usable_area * fertilizer_dose) / 10000  # kg
    necessary_seeds = ((usable_area * planting_density) / seed_purity) * seed_weight  # kg
    terrainData.EditTerrainDetail(total_area, usable_area,line_number, street_number, nitrogen_fertilizer, necessary_seeds)
    return terrainData

# Função para calcular as dimensões de área total, área util, número de linhas e número de ruas do terreno
def calculateTerrain(width, length, space_line, street_width): 
    total_area = width * length
    usable_area = total_area - (street_width * (length / space_line))
    line_number = math.ceil(usable_area / (space_line * width))
    street_number = math.ceil(width / (space_line + street_width))

    print(f"A área total {total_area} m²")
    print(f"A área útil {usable_area} m² (considerando ruas de {street_width}m e espaçamento entre linhas de {space_line}m)")
    print(f"O número de linhas {line_number:.0f}")
    print(f"O número de ruas {street_number:.0f}")

    return total_area, usable_area, line_number, street_number

# While principal onde roda toda a aplicação
while True:
    option = menuSelection()
    match option:
        case 1:
            get()
        case 2:
            insert()
        case 3:
            edit()
        case 4:
            delete()
        case 5:
            break
        case _:
            print("Opção inválida, tente novamente.\n")
    
    # Reseta todos os índices e reescreve o CSV
    df = df.reset_index(drop=True)
    df.to_csv('informacoes_culturas.csv', sep=';', index = False)