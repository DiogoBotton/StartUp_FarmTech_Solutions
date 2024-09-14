def escolher_cultura():
    while True:
        try:
            opcao = int(input("Escolha a cultura:\n1. Soja\n2. Café\n3. Sair\nDigite o número da opção: "))
            if 1 <= opcao <= 2:
                return opcao
            elif opcao == 3:
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Por favor, escolha entre 1 e 2.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def calcular_area_e_ruas(cultura, espaco_linha, largura_rua):
    largura = float(input("Digite a largura da área (em metros): "))
    while largura <= 0:
        print("A largura deve ser um valor positivo.")
        largura = float(input("Digite a largura da área (em metros): "))

    comprimento = float(input("Digite o comprimento da área (em metros): "))
    while comprimento <= 0:
        print("O comprimento deve ser um valor positivo.")
        comprimento = float(input("Digite o comprimento da área (em metros): "))

    area_total = largura * comprimento
    area_util = area_total - (largura_rua * (comprimento / espaco_linha))
    numero_linhas = area_util / (espaco_linha * largura)
    numero_ruas = largura / (espaco_linha + largura_rua)

    print(f"A área total é de {area_total} m²")
    print(f"A área útil é de {area_util} m² (considerando ruas de {largura_rua}m e espaçamento entre linhas de {espaco_linha}m)")
    print(f"O número de linhas é de {numero_linhas:.0f}")
    print(f"O número de ruas é de {numero_ruas:.0f}")

def main():
    cultura = escolher_cultura()
    if cultura:
        if cultura == 1:
            espaco_linha = 0.6
            largura_rua = 3.5
        elif cultura == 2:
            espaco_linha = 1.0
            largura_rua = 3.5
        calcular_area_e_ruas(cultura, espaco_linha, largura_rua)

if __name__ == "__main__":
    main()
