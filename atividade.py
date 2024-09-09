import csv

def escolher_cultura_e_calcular_area():
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
                print("Opção inválida. Por favor, escolha entre 1, 2, 3 ou 4.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def calcular_area_e_ruas(cultura):
    largura = float(input("Digite a largura da área (em metros): "))
    comprimento = float(input("Digite o comprimento da área (em metros): "))
    area_total = largura * comprimento

    largura_rua = 0

    # Definindo espaçamentos e largura de rua padrão (ajustável)
    if cultura == "soja":
        espaco_linha = 0.6  # Média entre 0.5 e 0.7
        largura_rua = 3.5  # Média entre 3 e 4
    elif cultura == "cafe":
        espaco_linha = 1.0  # Média entre 0.8 e 1.2
        largura_rua = 3.5  # Média entre 3 e 4

    print("Calculo da área do terreno")
    # Cálculo da área útil (considerando ruas)
    area_util = area_total - (largura_rua * (comprimento / espaco_linha))

    # Cálculo do número de linhas e ruas
    numero_linhas = area_util / (espaco_linha * largura)
    numero_ruas = largura / (espaco_linha + largura_rua)

    print(f"A área total é de {area_total} m²")
    print(f"A área útil é de {area_util} m² (considerando ruas de {largura_rua}m e espaçamento entre linhas de {espaco_linha}m)")
    print(f"O número de linhas é de {numero_linhas:.0f}")
    print(f"O número de ruas é de {numero_ruas:.0f}")

    return area_util

def calcular_insumos(area_util, cultura):
    # Definir doses e parâmetros para cada cultura
    if cultura == "soja":
        dose_adubo_N = 80  # kg/ha (ajuste conforme necessidade)
        pureza_sementes = 0.95
        densidade_plantio = 500000  # plantas/ha
        peso_por_semente = 0.2 / 1000  # Peso médio da semente de soja em kg (0.2 gramas por semente)
    elif cultura == "cafe":
        dose_adubo_N = 100  # kg/ha (ajuste conforme necessidade)
        pureza_sementes = 0.98
        densidade_plantio = 300000  # plantas/ha
        peso_por_semente = 0.05 / 1000  # Peso médio da semente de café em kg (0.05 gramas por semente)

    # Cálculos
    adubo_nitrogenado = (area_util * dose_adubo_N) / 10000  # kg
    sementes_necessarias = (area_util * densidade_plantio) / pureza_sementes  # unidades
    sementes_necessarias_kg = sementes_necessarias * peso_por_semente  # Convertendo para kg

    print(f"Quantidade de adubo nitrogenado: {adubo_nitrogenado:.2f} kg")
    print(f"Quantidade de sementes necessárias: {sementes_necessarias_kg:.2f} kg")

    return adubo_nitrogenado, sementes_necessarias_kg

def remover_informacao():
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
            del areas_uteis[indice]
            del adubos[indice]
            del sementes[indice]
            print("Informação removida com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")

def salvar_em_csv():
    # Abre o arquivo em modo 'append' para adicionar novas linhas
    with open('informacoes_culturas.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Verifica se o arquivo está vazio e adiciona o cabeçalho
        file.seek(0, 2)  # Move o cursor para o final do arquivo
        if file.tell() == 0:  # Verifica se o arquivo está vazio
            writer.writerow(["Cultura", "Área Útil (m²)", "Adubo Nitrogenado (kg)", "Sementes Necessárias (kg)"])
        # Grava as novas informações
        for i in range(len(culturas)):
            writer.writerow([culturas[i], f"{areas_uteis[i]:.2f}", f"{adubos[i]:.2f}", f"{sementes[i]:.2f}"])
    print("Informações salvas no arquivo 'informacoes_culturas.csv'.")

# Vetores para armazenar os resultados
culturas = []
areas_uteis = []
adubos = []
sementes = []

# Loop principal do programa
while True:
    cultura_escolhida = escolher_cultura_e_calcular_area()
    if cultura_escolhida is None:
        break  # Sai do loop se o usuário escolher sair
    elif cultura_escolhida == "remover":
        remover_informacao()
    else:
        area_util = calcular_area_e_ruas(cultura_escolhida)
        adubo_nitrogenado, sementes_necessarias_kg = calcular_insumos(area_util, cultura_escolhida)
        
        # Armazena os resultados nos vetores
        culturas.append(cultura_escolhida)
        areas_uteis.append(area_util)
        adubos.append(adubo_nitrogenado)
        sementes.append(sementes_necessarias_kg)

# Exibe os dados armazenados
print("\nDados armazenados:")
for i in range(len(culturas)):
    print(f"\nCultura: {culturas[i]}")
    print(f"Área útil: {areas_uteis[i]:.2f} m²")
    print(f"Adubo nitrogenado: {adubos[i]:.2f} kg")
    print(f"Sementes necessárias: {sementes[i]:.2f} kg")

# Salva os dados no arquivo CSV
salvar_em_csv()
