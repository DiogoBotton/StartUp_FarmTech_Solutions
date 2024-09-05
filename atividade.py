#A FarmTech Solutions fechou um contrato com uma fazenda que investe em inovação e tecnologia 
# para aumentar sua produtividade e pretende migrar para a Agricultura Digital. 
# E para atender esse importante cliente, a FarmTech vai começar a pôr a mão na massa, desenvolvendo 
# uma aplicação em Python que tenha:

#a. O projeto em Python deve dar suporte a 2 tipos de culturas. O grupo vai decidir quais culturas trabalhar. 
# Pense nas principais culturas do seu estado. 
    # Culturas escolhidas soja e café

"""""
def escolher_cultura():
    while True:
        try:
            opcao = int(input("Escolha a cultura:\n1. Soja\n2. Café\n3. Sair\nDigite o número da opção: "))
            if opcao == 1:
                return "soja"
            elif opcao == 2:
                return "café"
            elif opcao == 3:
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Por favor, escolha entre 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

# Chamando a função e imprimindo o resultado
cultura_escolhida = escolher_cultura()
if cultura_escolhida:
    print("Você escolheu:", cultura_escolhida)
"""

#b. Cálculo de área de plantio para cada cultura. O grupo decide qual tipo de figura geométrica 
# deve-se calcular como área plantada para cada tipo de cultura;
    # Optamos pela figura geometrica retangulo | talhões = divisão na plantação
""""
def escolher_cultura_e_calcular_area():
    while True:
        try:
            opcao = int(input("Escolha a cultura:\n1. Soja\n2. Café\n3. Sair\nDigite o número da opção: "))
            if opcao == 1:
                return "soja"
            elif opcao == 2:
                return "café"
            elif opcao == 3:
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Por favor, escolha entre 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def calcular_area_e_ruas(cultura):
    largura = float(input("Digite a largura da área (em metros): "))
    comprimento = float(input("Digite o comprimento da área (em metros): "))
    area_total = largura * comprimento

    # Definindo espaçamentos e largura de rua padrão (ajustável)
    if cultura == "soja":
        espaco_linha = 0.6  # Média entre 0.5 e 0.7
        largura_rua = 3.5  # Média entre 3 e 4
    elif cultura == "cafe":
        espaco_linha = 1.0  # Média entre 0.8 e 1.2
        largura_rua = 3.5  # Média entre 3 e 4

    # Cálculo da área útil (considerando ruas)
    # A área útil é calculada subtraindo a área ocupada pelas ruas da área total.
    area_util = area_total - (largura_rua * (comprimento / espaco_linha))

    # Cálculo do número de linhas e ruas
    numero_linhas = area_util / (espaco_linha * largura)
    numero_ruas = largura / (espaco_linha + largura_rua)

    print(f"A área total é de {area_total} m²")
    print(f"A área útil é de {area_util} m² (considerando ruas de {largura_rua}m e espaçamento entre linhas de {espaco_linha}m)")
    print(f"O número de linhas é de {numero_linhas:.0f}")
    print(f"O número de ruas é de {numero_ruas:.0f}")

# Chamando as funções
cultura_escolhida = escolher_cultura_e_calcular_area()
if cultura_escolhida:
    calcular_area_e_ruas(cultura_escolhida)

"""

#c. Cálculo do manejo de insumos. O grupo escolhe o tipo de cultura, o produto e a quantidade necessária,
# como por exemplo, aplicar fosfato no café e pulverizar 500 mL/metro com o trator. 
# Quantas ruas a lavoura têm? E assim, quantos litros serão necessários?


def escolher_cultura_e_calcular_area():
    while True:
        try:
            opcao = int(input("Escolha a cultura:\n1. Soja\n2. Café\n3. Sair\nDigite o número da opção: "))
            if opcao == 1:
                return "soja"
            elif opcao == 2:
                return "café"
            elif opcao == 3:
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Por favor, escolha entre 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def calcular_area_e_ruas(cultura):
    largura = float(input("Digite a largura da área (em metros): "))
    comprimento = float(input("Digite o comprimento da área (em metros): "))
    area_total = largura * comprimento

    # Definindo espaçamentos e largura de rua padrão (ajustável)
    if cultura == "soja":
        espaco_linha = 0.6  # Média entre 0.5 e 0.7
        largura_rua = 3.5  # Média entre 3 e 4
    elif cultura == "cafe":
        espaco_linha = 1.0  # Média entre 0.8 e 1.2
        largura_rua = 3.5  # Média entre 3 e 4

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
    elif cultura == "cafe":
        dose_adubo_N = 100  # kg/ha (ajuste conforme necessidade)
        pureza_sementes = 0.98
        densidade_plantio = 300000  # plantas/ha

    # Cálculos
    adubo_nitrogenado = (area_util * dose_adubo_N) / 10000  # kg
    sementes_necessarias = (area_util * densidade_plantio) / pureza_sementes  # unidades

    print(f"Quantidade de adubo nitrogenado: {adubo_nitrogenado:.2f} kg")
    print(f"Quantidade de sementes necessárias: {sementes_necessarias:.0f} unidades")

# Chamando as funções
cultura_escolhida = escolher_cultura_e_calcular_area()
if cultura_escolhida:
    area_util = calcular_area_e_ruas(cultura_escolhida)
    calcular_insumos(area_util, cultura_escolhida)

