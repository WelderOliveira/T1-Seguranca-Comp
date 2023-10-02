# Defina o alfabeto usado na cifra, incluindo espaço em branco
alfabeto = 'abcdefghijklmnopqrstuvwxyz'


# Função para cifrar uma mensagem
def cifrar(mensagem, chave):
    mensagem = filtrar_caracteres_invalidos(mensagem)
    mensagem_em_lista = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    encriptado = ''
    for msg in mensagem_em_lista:
        for letra, chave_letra in zip(msg, chave):
            indice = (alfabeto.index(letra.lower()) + alfabeto.index(chave_letra.lower())) % len(alfabeto)
            encriptado += alfabeto[indice].upper() if letra.isupper() else alfabeto[indice]

    return encriptado


# Função para decifrar uma mensagem cifrada
def decifrar(mensagem, chave):
    mensagem = filtrar_caracteres_invalidos(mensagem)
    mensagem_em_lista = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    decriptado = ''
    for msg in mensagem_em_lista:
        for letra, chave_letra in zip(msg, chave):
            indice = (alfabeto.index(letra.lower()) - alfabeto.index(chave_letra.lower())) % len(alfabeto)
            decriptado += alfabeto[indice].upper() if letra.isupper() else alfabeto[indice]

    return decriptado


# Função para filtrar caracteres inválidos e manter apenas os caracteres do alfabeto
def filtrar_caracteres_invalidos(mensagem):
    return ''.join(c for c in mensagem if c in alfabeto)


# Função principal para entrada e saída de dados
def main():
    while True:
        select = int(
            input(
                'Selecione o que deseja fazer \n 1 - Criptografar \n 2 - Decriptografar \n 3 - Atacar \n 4 - Sair \n '
                '-> '))

        if select == 1:
            # Solicita ao usuário a entrada do texto a ser cifrado e a chave
            msg = input('Digite o texto a ser cifrado: ').lower()
            chave = input('Digite a chave: ').lower()

            # Cifra e imprime o texto
            texto_cifrado = cifrar(msg, chave)
            print('Texto cifrado:', texto_cifrado.upper())
        elif select == 2:
            # Solicita ao usuário a entrada do texto a ser decifrado e a chave
            msg = input('Digite o texto a ser decifrado: ').lower()
            chave = input('Digite a chave: ').lower()

            # Decifra e imprime o texto
            texto_decifrado = decifrar(msg, chave)
            print('Texto decifrado:', texto_decifrado.upper())
        elif select == 3:
            pass
        else:
            exit()


if __name__ == '__main__':
    main()
