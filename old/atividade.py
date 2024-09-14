import csv
from tabulate import tabulate

#Lê arquivo CSV e retorna os dados em lista.

def ler_csv(arquivo):
     
    with open(arquivo, mode='r') as file:
        reader = csv.reader(file)
        dados = list(reader)
    return dados

def dados_armazenados():
    
#Mostra na tela os dados armazenados em formato de tabela.
    
    dados_csv = ler_csv('informacoes_culturas.csv')
    if dados_csv:
        cabecalho = ["Cultura", "Largura (m)", "Comprimento (m)", "AreaTotal (m²)", "AreaUtil (m²)", "AduboNitrogenado (kg)", "SementesNecessarias (kg)"]
        print("Veja os dados armazenados")
        print(tabulate(dados_csv, headers=cabecalho, tablefmt='fancy_grid', floatfmt=".2f", numalign="right"))
    else:
        print("Nenhum dado armazenado encontrado.")

def main():
    while True:
        opcao = input("Deseja ver os dados armazenados? (s/n): ").strip().lower()
        if opcao == 's':
            dados_armazenados()
        elif opcao == 'n':
            break
        else:
            print("Opção inválida. Digite 's' para Sim ou 'n' para Não.")

    while True:
        cultura = cultura_calcular_area()
        if cultura is None:
            break
        elif cultura == "remover":
            remover_info()
        else:
            largura = float(input("Digite a largura do terreno (em metros): "))
            comprimento = float(input("Digite o comprimento do terreno (em metros): "))
            espaco_linha = float(input("Digite o espaçamento entre linhas (em metros): "))
            largura_rua = float(input("Digite a largura das ruas (em metros): "))

            largura, comprimento, area_total, area_util = area_ruas(largura, comprimento, espaco_linha, largura_rua)
            adubo_nitrogenado, sementes_necessarias = calcular_insumos(area_util, cultura)

            print(f"Para a cultura de {cultura}, você precisará de {adubo_nitrogenado:.2f} kg de adubo nitrogenado e {sementes_necessarias:.2f} kg de sementes.")

            # Armazena os resultados nos vetores
            culturas.append(cultura)
            larguras.append(largura)
            comprimentos.append(comprimento)
            areas_totais.append(area_total)
            areas_uteis.append(area_util)
            adubos.append(adubo_nitrogenado)
            sementes.append(sementes_necessarias)

# Deseja inserir mais dados
            inserir_mais = input("Deseja inserir mais dados? (s/n): ").strip().lower()
            if inserir_mais != 's':
                break
            print("Você saiu do programa.")

# Salva os dados no arquivo CSV após o loop
    salvar_csv()

# Pergunta ao usuário se deseja visualizar os dados armazenados
    opcao = input("Deseja ver os dados armazenados? (s/n): ").strip().lower()
    if opcao == 's':
        dados_armazenados()
    elif opcao == 'n':
        print("Programa finalizado.")

def cultura_calcular_area():
    while True:
        try:
            opcao = int(input("Escolha a cultura:\n1. Soja\n2. Café\n3. Sair\n4. Remover informação\nDigite o número da opção: "))
            if opcao == 1:
                return "soja"
            elif opcao == 2:
                return "cafe"
            elif opcao == 3:
                print("Saindo do programa.")
                return None  # Retorna None para indicar que o usuário escolheu sair
            elif opcao == 4:
                return "remover"
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
        except ValueError:
            print("Opção inválida. Por favor, digite um número.")

#Calcula a área total e útil do terreno
def area_ruas(largura, comprimento, espaco_linha, largura_rua):
      
    area_total = largura * comprimento
    numero_linhas = comprimento / espaco_linha
    numero_ruas = largura / (espaco_linha + largura_rua)
    area_util = area_total - (numero_ruas * largura_rua * comprimento)

    print(f"A área total {area_total} m²")
    print(f"A área útil {area_util} m² (considerando ruas de {largura_rua}m e espaçamento entre linhas de {espaco_linha}m)")
    print(f"O número de linhas {numero_linhas:.0f}")
    print(f"O número de ruas {numero_ruas:.0f}")

    return largura, comprimento, area_total, area_util

#Calcula a quantidade de adubo nitrogenado e sementes necessárias para uma determinada cultura.
def calcular_insumos(area_util, cultura):  
   
# Definir doses e parâmetros para cada cultura
    if cultura == "soja":
        dose_adubo_N = 80  # kg/ha 
        pureza_sementes = 0.95
        densidade_plantio = 500000  # plantas/ha
        peso_por_semente = 0.2 / 1000  # Peso médio da semente de soja em kg (0.2 gramas por semente)
    elif cultura == "cafe":
        dose_adubo_N = 100  # kg/ha 
        pureza_sementes = 0.98
        densidade_plantio = 300000  # plantas/ha
        peso_por_semente = 0.05 / 1000  # Peso médio da semente de café em kg (0.05 gramas por semente)

# Cálculos
    adubo_nitrogenado = (area_util * dose_adubo_N) / 10000  # kg
    sementes_necessarias = (area_util * densidade_plantio) / pureza_sementes  # unidades

    return adubo_nitrogenado, sementes_necessarias

def remover_info():
    if len(culturas) == 0:
        print("Nenhuma informação disponível para remover.")
        return
    
    print("\nInformações disponíveis para remoção:")
    for i in range(len(culturas)):
        print(f"{i + 1}. Cultura: {culturas[i]}, Área útil: {areas_uteis[i]:.2f} m²")

    try:
        indice = int(input("Digite o número da informação que deseja remover: ")) - 1
        if 0 <= indice < len(culturas):
            del culturas[indice]
            del larguras[indice]
            del comprimentos[indice]
            del areas_totais[indice]
            del areas_uteis[indice]
            del adubos[indice]
            del sementes[indice]
            print("Informação removida com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")

# Abre o arquivo em modo 'append' para adicionar novas linhas
# Verifica se o arquivo está vazio e adiciona o cabeçalho
# Adiciona as informações no arquivo
def salvar_csv():
    
    with open('informacoes_culturas.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        file.seek(0, 2)  
        if file.tell() == 0:  # 
            writer.writerow(["Cultura", "Largura (m)", "Comprimento (m)", "AreaTotal (m²)", "AreaUtil (m²)", "AduboNitrogenado (kg)", "SementesNecessarias (kg)"])

        for i in range(len(culturas)):
            writer.writerow([culturas[i], f"{larguras[i]:.2f}", f"{comprimentos[i]:.2f}", f"{areas_totais[i]:.2f}", f"{areas_uteis[i]:.2f}", f"{adubos[i]:.2f}", f"{sementes[i]:.2f}"])
        print("Informações salvas no arquivo 'informacoes_culturas.csv'.")

# Listas para armazenar os dados
culturas = []
larguras = []
comprimentos = []
areas_totais = []
areas_uteis = []
adubos = []
sementes = []

if __name__ == "__main__":
    main()