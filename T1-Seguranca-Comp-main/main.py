# Define o alfabeto usado na cifra, incluindo espaço em branco
alfabeto = 'abcdefghijklmnopqrstuvwxyz'

# Frequências de letras em inglês e português
frequencias_ingles = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
                      0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                      0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

frequencias_portugues = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128, 0.0618, 0.040, 0.002,
                         0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.0120, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167,
                         0.001, 0.0021, 0.001, 0.0047]

utilizar_frequencias_portugues = False


def cifrar(mensagem, chave):
    """
    Cifra uma mensagem usando a cifra de Vigenère.

    Args:
        mensagem (str): A mensagem a ser cifrada.
        chave (str): A chave para a cifra.

    Returns:
        str: A mensagem cifrada.
    """
    # Remove caracteres inválidos da mensagem a ser cifrada
    mensagem = filtrar_caracteres_invalidos(mensagem)

    # Divide a mensagem em blocos com o mesmo tamanho da chave
    mensagem_em_blocos = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    # Inicializa uma string vazia para armazenar a mensagem cifrada
    mensagem_cifrada = ''

    # Itera sobre cada bloco da mensagem
    for bloco in mensagem_em_blocos:
        # Itera sobre cada letra do bloco e a letra correspondente da chave
        for letra, chave_letra in zip(bloco, chave):
            # Calcula o índice da letra cifrada usando a fórmula da cifra de Vigenère
            indice = (alfabeto.index(letra.lower()) + alfabeto.index(chave_letra.lower())) % len(alfabeto)

            # Adiciona a letra cifrada à mensagem cifrada, mantendo a caixa (maiúscula/minúscula)
            mensagem_cifrada += alfabeto[indice].upper() if letra.isupper() else alfabeto[indice]

    # Retorna a mensagem cifrada
    return mensagem_cifrada


def decifrar(mensagem, chave):
    """
    Decifra uma mensagem cifrada usando a cifra de Vigenère.

    Args:
        mensagem (str): A mensagem cifrada.
        chave (str): A chave usada na cifragem.

    Returns:
        str: A mensagem decifrada.
    """
    # Remove caracteres inválidos da mensagem cifrada
    mensagem = filtrar_caracteres_invalidos(mensagem)

    # Divide a mensagem em blocos com o mesmo tamanho da chave
    mensagem_em_blocos = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    # Inicializa uma string vazia para armazenar a mensagem decifrada
    mensagem_decifrada = ''

    # Itera sobre cada bloco da mensagem
    for bloco in mensagem_em_blocos:
        # Itera sobre cada letra do bloco e a letra correspondente da chave
        for letra, chave_letra in zip(bloco, chave):
            # Calcula o índice da letra decifrada usando a fórmula da cifra de Vigenère
            indice = (alfabeto.index(letra.lower()) - alfabeto.index(chave_letra.lower())) % len(alfabeto)

            # Adiciona a letra decifrada à mensagem decifrada, mantendo a caixa (maiúscula/minúscula)
            mensagem_decifrada += alfabeto[indice].upper() if letra.isupper() else alfabeto[indice]

    # Retorna a mensagem decifrada
    return mensagem_decifrada


def analisar_frequencia(sequencia):
    """
    Analisa a frequência de letras em uma sequência de texto.

    Args:
        sequencia (str): A sequência de texto a ser analisada.

    Returns:
        str: A letra escolhida com base na análise de frequência.
    """
    todos_qui_quadrados = [0] * 26

    for i in range(26):
        sequencia_deslocada = [alfabeto[(alfabeto.index(letra.lower()) - i) % 26] for letra in sequencia]

        frequencias_ocorrencias_letras = [float(sequencia_deslocada.count(letra)) / float(len(sequencia)) for letra in
                                          alfabeto]

        soma_qui_quadrado = 0.0
        frequencia = frequencias_portugues if utilizar_frequencias_portugues else frequencias_ingles
        for j in range(26):
            soma_qui_quadrado += ((frequencias_ocorrencias_letras[j] - float(frequencia[j])) ** 2) / float(
                frequencia[j])

        todos_qui_quadrados[i] = soma_qui_quadrado

    letra_com_menor_qui_quadrado = todos_qui_quadrados.index(min(todos_qui_quadrados))

    for qui_quadrado in sorted(todos_qui_quadrados)[:5]:
        print(f'({alfabeto[todos_qui_quadrados.index(qui_quadrado)]}:{qui_quadrado:.2f})', end=' ')
    letra = input('Escolha uma letra ou aperte enter: ')
    return letra if len(letra) == 1 and letra in alfabeto else alfabeto[letra_com_menor_qui_quadrado]


def obter_chave(mensagem, tamanho_chave):
    chave = ''

    for i in range(tamanho_chave):
        sequencia = ''

        # Coleta caracteres da mensagem a cada 'tamanho_chave' de deslocamento
        for j in range(i, len(mensagem), tamanho_chave):
            sequencia += mensagem[j]

        # Utiliza a análise de frequência para determinar a letra da chave
        chave += analisar_frequencia(sequencia)

    return chave


def calcular_indice_coincidencia(sequencia):
    N = len(sequencia)
    soma_frequencia = 0.0

    for letra in alfabeto:
        ocorrencias = sequencia.count(letra)
        soma_frequencia += ocorrencias * (ocorrencias - 1)  # Evita a repetição da contagem

    indice_coincidencia = soma_frequencia / (N * (N - 1))

    return indice_coincidencia


def encontrar_tamanho_chave(mensagem, tamanho_maximo=20):
    # Inicializa uma lista vazia para armazenar os índices de coincidência média
    indices_coincidencia = []

    # Define o tamanho máximo para procurar supostos tamanhos de chave
    tamanho_maximo_chave = tamanho_maximo

    # Loop que itera sobre supostos tamanhos de chave
    for tamanho_suposto in range(tamanho_maximo_chave):
        # Inicializa a soma dos índices de coincidência
        soma_indices_coincidencia = 0.0

        # Loop que itera sobre as posições de caracteres dentro de um bloco do tamanho_suposto
        for posicao_inicial in range(tamanho_suposto):
            sequencia = ''

            # Loop que constrói uma sequência de caracteres de acordo com o tamanho_suposto
            for indice_caractere in range(posicao_inicial, len(mensagem), tamanho_suposto):
                sequencia += mensagem[indice_caractere]

            # Verifica se a sequência tem mais de um caractere antes de calcular o índice de coincidência
            if len(sequencia) > 1:
                soma_indices_coincidencia += calcular_indice_coincidencia(sequencia)

        # Calcula o índice de coincidência médio para o tamanho_suposto atual
        ic_medio = soma_indices_coincidencia / tamanho_suposto if not tamanho_suposto == 0 else 0.0

        # Adiciona o índice de coincidência médio à tabela de índices de coincidência
        indices_coincidencia.append(ic_medio)

    # Ordena a tabela de índices de coincidência em ordem decrescente
    indices_coincidencia_ordenados = sorted(indices_coincidencia, reverse=True)

    # Encontra os melhores supostos tamanhos de chave com base nos índices de coincidência ordenados
    melhores_suposicoes = list(map(lambda valor: indices_coincidencia.index(valor), indices_coincidencia_ordenados))

    # Remove valores duplicados e zeros dos melhores supostos tamanhos de chave
    melhores_suposicoes = [suposicao for suposicao in list(dict.fromkeys(melhores_suposicoes)) if suposicao != 0]

    # Retorna uma lista dos melhores supostos tamanhos de chave (os 5 primeiros)
    return melhores_suposicoes[:5]


def atacar(mensagem):
    # Filtra caracteres inválidos da mensagem
    mensagem = filtrar_caracteres_invalidos(mensagem)

    # Encontra os tamanhos de chave mais prováveis na mensagem
    tamanhos_chave = encontrar_tamanho_chave(mensagem)

    # Verifica se não foram encontrados tamanhos de chave
    if not tamanhos_chave:
        return None
    else:
        # Imprime os tamanhos de chave encontrados (em ordem de possível melhor tamanho)
        print('Tamanhos de chaves encontradas (em ordem de possível melhor tamanho): ',
              *[{i: tamanhos_chave[i]} for i in range(len(tamanhos_chave))])

        # Solicita ao usuário que escolha um tamanho de chave ou pressione Enter para usar o primeiro tamanho
        tamanho_escolhido = input('Escolha uma começando do índice 0 ou aperte enter: ')

        # Converte a escolha do usuário para um valor numérico
        tamanho_escolhido = int(tamanho_escolhido) % len(tamanhos_chave) if tamanho_escolhido.isnumeric() else 0

        # Obtém a chave usando o tamanho de chave escolhido
        chave = obter_chave(mensagem, tamanhos_chave[tamanho_escolhido])

        # Retorna a chave obtida
        return chave


def filtrar_caracteres_invalidos(mensagem):
    return ''.join(c for c in mensagem if c in alfabeto)


def main():
    global utilizar_frequencias_portugues

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
            mensagem = input('Digite o texto a ser atacado: ').lower()
            utilizar_opcao = input('Utilizar frequências em português [s/n]? ')
            if utilizar_opcao.lower() in 'simyes' and len(utilizar_opcao) > 0:
                utilizar_frequencias_portugues = True
            chave = atacar(mensagem)
            if chave:
                resultado = decifrar(mensagem, chave)
                print(resultado)
        else:
            exit()


if __name__ == '__main__':
    main()
