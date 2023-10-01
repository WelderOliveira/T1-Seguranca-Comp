# Defina o alfabeto usado na cifra, incluindo espaço em branco
alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '


# Função para cifrar uma mensagem
def cifrar(texto, chave):
    texto_cifrado = ''
    i = 0

    for i in range(len(texto)):
        if texto[i] in alfabeto:
            # Encontre o índice da letra atual na mensagem e da letra correspondente na chave
            indice_letra = alfabeto.find(texto[i])
            indice_chave = alfabeto.find(chave[i % len(chave)])

            # Calcule o novo índice usando a cifra de Vigenère
            novo_indice = (indice_letra + indice_chave) % len(alfabeto)

            # Adicione a letra cifrada ao texto cifrado
            texto_cifrado += alfabeto[novo_indice]
            i += 1
        else:
            # Se não for uma letra do alfabeto, mantenha o caractere original
            texto_cifrado += texto[i]

    return texto_cifrado


# Função para decifrar uma mensagem cifrada
def decifrar(frase_cifrada, chave):
    texto_decifrado = ''
    i = 0

    for letra in frase_cifrada:
        # Verifique se a letra cifrada está no alfabeto
        if letra in alfabeto:
            # Encontre o índice da letra cifrada atual na mensagem e da letra correspondente na chave
            indice_letra_cifrada = alfabeto.find(letra)
            indice_chave = alfabeto.find(chave[i % len(chave)])

            # Calcule o novo índice usando a cifra de Vigenère
            novo_indice = (indice_letra_cifrada - indice_chave) % len(alfabeto)

            # Se o resultado for negativo, adicione o tamanho do alfabeto para obter um índice positivo
            if novo_indice < 0:
                novo_indice += len(alfabeto)

            # Adicione a letra decifrada ao texto decifrado
            texto_decifrado += alfabeto[novo_indice]
        else:
            # Se a letra cifrada não estiver no alfabeto, mantenha-a no texto decifrado
            texto_decifrado += letra
        i += 1

    return texto_decifrado


# Função principal para entrada e saída de dados
def main():
    while True:
        select = int(
            input(
                'Selecione o que deseja fazer \n 1 - Criptografar \n 2 - Decriptografar \n 3 - Atacar \n 4 - Sair \n '
                '-> '))

        if select == 1:
            # Solicita ao usuário a entrada do texto a ser cifrado e a chave
            msg = str(input('Digite o texto a ser cifrado: ')).upper()
            msg = msg.replace(',', "").replace('.', "").replace('-', "").replace('"', "").replace(':', "").replace(';',
                                                                                                                   "").replace(
                "'", "")
            chave = str(input('Digite a chave: ')).upper()

            # Cifra e imprime o texto
            texto_cifrado = cifrar(msg, chave)
            print('Texto cifrado:', texto_cifrado)
        elif select == 2:
            # Solicita ao usuário a entrada do texto a ser decifrado e a chave
            msg = str(input('Digite o texto a ser decifrado: ')).upper()
            msg = msg.replace(',', "").replace('.', "").replace('-', "").replace('"', "").replace(':', "").replace(';',
                                                                                                                   "").replace(
                "'", "")
            chave = str(input('Digite a chave: ')).upper()

            # Decifra e imprime o texto
            texto_decifrado = decifrar(msg, chave)
            print('Texto decifrado:', texto_decifrado)
        elif select == 3:
            pass
        else:
            exit()


if __name__ == '__main__':
    main()
