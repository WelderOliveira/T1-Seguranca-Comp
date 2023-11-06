from random import randint  # usado apenas para gerar chave de 16 bytes com valores aleatorios entre 0x0 e 0xFF

################################################################################################
# TABELAS S_BOX, RCON
# tabela de subtituicao com todas as combinacoes de 0 a 255 util para geracao de subchaves e aes
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

# tabela rcon util para gerar subchaves
r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
    0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
    0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
    0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
    0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
    0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
    0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
    0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
    0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
    0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
)


def flatten(lista):
    """
    Nivela uma lista que contém sub-listas, transformando-a em uma lista plana.

    :param lista: Lista contendo sub-listas.
    :return: Lista plana.
    """
    return [item for sublista in lista for item in sublista]


def gerar_hexadecimal(valores):
    hex_valores = [hex(valor) for valor in valores]
    hex_string = ' '.join(hex_valores)
    return hex_string


def criar_blocos_jpg(lista_de_bytes):
    sos_marker = {}

    # Procura o marcador "Start of Scan" (0xffda)
    for i in range(len(lista_de_bytes) - 1):
        if lista_de_bytes[i] == 0xff and lista_de_bytes[i + 1] == 0xda:
            sos_marker['comeco'] = i + 1
            sos_marker['tamanho'] = (lista_de_bytes[i + 2] * 256) + lista_de_bytes[i + 3]
            break  # Considera apenas o primeiro marcador "Start of Scan" encontrado

    # Determina o início e o fim dos dados do bloco
    inicio_dados_bloco = sos_marker['comeco'] + sos_marker['tamanho'] + 1
    fim_dados_bloco = -2  # Em um arquivo JPG normal, os 2 últimos bytes são 0xffd9, indicando o fim do JPG
    image_data = lista_de_bytes[inicio_dados_bloco:fim_dados_bloco]

    # Remove bytes 0x00 após 0xff, se houver
    for i in range(0, len(image_data) - 1):
        if image_data[i] == 0xff and image_data[i + 1] == 0x00:
            image_data[i + 1] = None

    # Remove valores None (0x00) que acompanham 0xff (0xff 0x00 == 0xff em JPG)
    image_data = [value for value in image_data if value is not None]

    # Divide os dados em blocos de 16 bytes
    blocos = []
    for i in range(0, len(image_data), 16):
        novo_bloco = image_data[i:i + 16]
        if len(novo_bloco) < 16:
            preencher_restante = [0x0] * (16 - len(novo_bloco))  # Adiciona padding
            novo_bloco += preencher_restante
        blocos.append(novo_bloco.copy())

    sos_marker['blocos'] = blocos.copy()

    return sos_marker


def substituir_bytes_jpg(parte_modificada):
    nova_parte = []
    for byte in parte_modificada:
        nova_parte.append(byte)
        if byte == 0xFF:
            nova_parte.append(0x00)
    return nova_parte


def gerar_subchaves(chave, rodadas):
    # Divide a chave em palavras de 4 bytes
    subchaves = dividir_chave_palavras(chave)

    for i in range(4, (4 * rodadas) + 4):
        if i % 4 == 0:
            # Rotaciona a subchave anterior e realiza a operação SubBytes
            nova_subchave = rotacionar_palavra(subchaves[i - 1], 1)
            nova_subchave = sub_bytes(nova_subchave)
            nova_subchave = xor_com_rcon(nova_subchave, i // 4, r_con)

        # XOR da nova subchave com a subchave 4 posições atrás
        nova_subchave = xor_entre_palavras(nova_subchave, subchaves[i - 4])

        subchaves.append(nova_subchave)

    return subchaves


def xor_entre_palavras(palavra1, palavra2):
    # Certifica de que ambas as palavras tenham o mesmo tamanho
    if len(palavra1) != len(palavra2):
        raise ValueError("As palavras devem ter o mesmo tamanho para realizar a operação XOR")

    resultado = []

    for byte1, byte2 in zip(palavra1, palavra2):
        resultado.append(byte1 ^ byte2)  # Realiza o XOR byte a byte

    return resultado


def dividir_chave_palavras(chave):
    palavras = []
    for i in range(0, len(chave), 4):
        palavra = chave[i:i + 4]
        palavras.append(palavra)
    return palavras


def rotacionar_palavra(palavra, n):
    return palavra[n:] + palavra[0:n]


def xor_com_rcon(palavra, pos, rcon):
    return [palavra[0] ^ rcon[pos % len(rcon)]] + palavra[1:]


def pegar_chave_da_rodada(subchaves, rodada):
    """
    Seleciona as 4 subchaves da rodada e concatena em uma única chave de 16 bytes.

    :param subchaves: Lista de subchaves do AES.
    :param rodada: Número da rodada (0, 1, 2, ...).
    :return: A chave da rodada como uma lista de 16 bytes.
    """
    inicio = rodada * 4
    fim = inicio + 4
    chave_da_rodada = []

    for i in range(inicio, fim):
        chave_da_rodada.extend(subchaves[i])

    return chave_da_rodada


def pegar_matriz_transposta(matriz):
    matriz_transposta = []

    for i in range(4):
        for j in range(4):
            matriz_transposta.append(matriz[(4 * j) + i])

    return matriz_transposta


# FUNÇÕES AES
##########################################################
# Função de substituição de bytes
def sub_bytes(palavra):
    resultado = []
    for pos in palavra:
        resultado.append(s_box[pos])
    return resultado


# Função de permutação de linhas
def shift_rows(estado):
    """
    Realiza a operação de permutação de linhas no estado do AES.

    :param estado: Uma lista de 16 bytes representando o estado.
    :return: O estado com as linhas permutadas.
    """
    estado_permutado = []

    for i in range(4):
        linha_rotacionada = rotacionar_palavra(estado[i * 4:(i * 4) + 4], i)
        estado_permutado.extend(linha_rotacionada)

    return estado_permutado


def mix_columns(estado):
    """
    Realiza a operação de mistura de colunas no estado do AES.

    :param estado: Uma lista de 16 bytes representando o estado.
    :return: O estado com as colunas misturadas.
    """
    matriz_mistura = [
        2, 3, 1, 1,
        1, 2, 3, 1,
        1, 1, 2, 3,
        3, 1, 1, 2
    ]

    novo_estado = [0] * 16

    for coluna in range(4):
        for linha in range(4):
            for i in range(4):
                novo_estado[coluna + linha * 4] ^= galois_multiplicacao(matriz_mistura[i + linha * 4],
                                                                        estado[coluna + i * 4])

    return novo_estado


def galois_multiplicacao(a, b):
    """
    Realiza a multiplicação de Galois entre dois números.

    :param a: Primeiro número.
    :param b: Segundo número.
    :return: O resultado da multiplicação de Galois.
    """
    resultado = 0
    while b:
        if b & 1:
            resultado ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= 0x11B  # Máscara fixa para Galois Field (AES Polynomial)
    return resultado


# Função de adição da chave da rodada
def add_round_key(estado, chave_da_rodada):
    """
    Adiciona a chave da rodada ao estado usando a operação XOR.

    :param estado: O estado atual.
    :param chave_da_rodada: A chave da rodada a ser adicionada.
    :return: O estado após a adição da chave.
    """
    novo_estado = [estado[i] ^ chave_da_rodada[i] for i in range(16)]
    return novo_estado


# Função principal de cifragem AES
def aes_cifrar(estado, chave, rodadas):
    # Chave inicial (Round 0)
    chave_da_rodada = pegar_chave_da_rodada(chave, 0)
    estado = add_round_key(estado, chave_da_rodada)

    for rodada in range(1, rodadas):
        # SubBytes
        estado = sub_bytes(estado)

        # ShiftRows
        estado = shift_rows(estado)

        # MixColumns
        estado = mix_columns(estado)

        # AddRoundKey
        chave_da_rodada = pegar_chave_da_rodada(chave, rodada)
        estado = add_round_key(estado, chave_da_rodada)

    # Última rodada
    estado = sub_bytes(estado)
    estado = shift_rows(estado)
    chave_final = pegar_chave_da_rodada(chave, rodadas)
    estado = add_round_key(estado, chave_final)

    return estado


##########################################################
def incrementar(contador):
    # Inicia a incrementação pelo último byte (menos significativo)
    i = len(contador) - 1

    while i >= 0:
        # Incrementa o byte atual
        contador[i] += 1

        # Se houver um overflow (o byte se torna 0x100), continue incrementando o próximo byte
        if contador[i] > 0xFF:
            contador[i] = 0x00
            i -= 1
        else:
            break

    return contador


def ctr(chave, blocos, rodadas):
    subchaves = gerar_subchaves(chave, rodadas)
    contador = [0x0] * 16

    blocos_gerados = []

    for bloco in blocos:
        contador_cifrada = aes_cifrar(pegar_matriz_transposta(contador.copy()), subchaves, rodadas)
        novo_bloco = xor_entre_palavras(contador_cifrada, bloco)
        blocos_gerados.append(novo_bloco)
        contador = incrementar(contador.copy())

    return blocos_gerados


def main():
    while True:
        opcao = input('Modo de execucao\n1 - para cifrar\n2 - para decifrar\nOpcao: ')

        if opcao not in ['1', '2']:
            print('Opcao invalida.')
            continue

        nome_imagem_entrada = str(
            input('Insira o caminho da imagem com extensao .jpg em que sera aplicado o algoritmo: '))
        rodadas = int(input('Quantidade de rodadas: '))
        chave = input(
            'Informe a chave (16 bytes separados por espaço) ou gere automaticamente (pressione enter): ').split()

        if not rodadas > 0 and not rodadas < 250:
            print('Excedeu o valor de rodada maximo (250)')
            continue

        if '.jpg' in nome_imagem_entrada:
            with open(nome_imagem_entrada, mode='rb') as original_file:
                original_image = list(original_file.read())
            # dict sos marker que contem blocos a ser cifrados, inicio do marcador e tamanho do marcador -> jpg
            sos_marker_info = criar_blocos_jpg(original_image.copy())
            # cabecalho da nova imagem
            nova_imagem = original_image.copy()[0:sos_marker_info['comeco'] + sos_marker_info['tamanho'] + 1]
            blocos = sos_marker_info['blocos'].copy()  # blocos de 16 bytes jpg

        else:
            print('Extensão da imagem não identificada.')
            continue

        if len(chave) == 16:
            chave = [int(value, 16) for value in chave]
        else:
            chave = [randint(0, 255) for _ in range(16)]

        print('Chave:', gerar_hexadecimal(chave))
        print('Realizando operações. Aguarde.')

        nome_imagem_saida = nome_imagem_entrada[0:-4] + '-'
        blocos_gerados = []  # blocos modificados

        if opcao == '1':  # cifrar
            nome_imagem_saida += 'cifrar'
            blocos_gerados = ctr(chave, blocos, rodadas)

        elif opcao == '2':  # decifrar
            nome_imagem_saida += 'decifrar'
            blocos_gerados = ctr(chave, blocos, rodadas)

        bloco_unico = flatten(blocos_gerados)  # Union blocks

        if '.jpg' in nome_imagem_entrada:
            nova_imagem += substituir_bytes_jpg(bloco_unico)  # montando jpg
            nova_imagem += [0xff, 0xd9]  # adiciona o marcador do final da imagem
            out_file_image = open(f'{nome_imagem_saida}.jpg', mode='wb')  # salvando jpg
            out_file_image.write(bytes(nova_imagem))
            out_file_image.close()

        print(f'Imagem resultante salva em: {nome_imagem_saida}')
        print('Finalizado!')
        break


if __name__ == '__main__':
    main()
