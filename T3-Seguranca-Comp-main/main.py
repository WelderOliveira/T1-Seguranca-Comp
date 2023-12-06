import base64
import math
import random
import secrets
import hashlib
from math import gcd


def mod_exp(base, exp, mod):
    # Função para calcular (base^exp) % mod usando exponenciação modular
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result


def miller_rabin_test(n, k=5):
    # Função principal para o teste de Miller-Rabin
    # n: número a ser testado
    # k: número de iterações (quanto maior, menor a probabilidade de erro)

    # Casos base para números pequenos
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Escreve n como (2^r * s + 1)
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    # Realiza o teste de Miller-Rabin k vezes
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_exp(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            # Se nenhum teste indicar que n é composto, retorna False
            return False

    # Se passou por todos os testes, n é provavelmente primo
    return True


def gerar_chave_prima(tamanho_chave):
    while True:
        possivel_chave = secrets.randbits(tamanho_chave)
        # Garante que a chave seja ímpar
        possivel_chave |= 1
        if miller_rabin_test(possivel_chave):
            return possivel_chave


def gerar_e(t, n):
    while True:
        possivel_e = secrets.randbelow(t)
        if gcd(possivel_e, t) == 1 and gcd(possivel_e, n) == 1:
            return possivel_e


def gerar_chave_rsa(tamanho_chave):
    # Gera dois números primos p e q
    p = gerar_chave_prima(tamanho_chave)
    q = gerar_chave_prima(tamanho_chave)

    # Calcula n (produto de p e q)
    n = p * q

    # Calcula φ(n) (totiente de n)
    phi_n = (p - 1) * (q - 1)

    # Escolhe um expoente público e calcula o expoente privado
    e = gerar_e(phi_n, n)  # Valor comum para e
    d = calcular_expoente_privado(e, phi_n)

    # Cria a chave pública
    chave_publica = (n, e)

    # Cria a chave privada
    chave_privada = (n, d)

    return chave_publica, chave_privada


def calcular_expoente_privado(e, phi_n):
    d, x, y = extended_gcd(e, phi_n)
    if d != 1:
        return None  # No modular inverse exists
    else:
        return x % phi_n


def extended_gcd(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0

    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1

    return b, x0, y0


def pad_message(message, key_length):
    # Aplica o preenchimento OEAP na mensagem.
    if len(message) > key_length - 2 * math.ceil(math.log2(key_length) / 8) - 2:
        raise ValueError("Tamanho da mensagem excede o limite suportado.")

    # Calcula o comprimento do preenchimento
    pad_length = key_length - len(message) - 2 * math.ceil(math.log2(key_length) / 8) - 2

    # Cria o preenchimento com 0x00 seguido por 0x01
    padding = b"\x00" * pad_length + b"\x01"

    # Adiciona o preenchimento à mensagem
    padded_message = b"\x00" + padding + message

    return padded_message


def unpad_message(padded_message):
    # Remove o preenchimento OEAP da mensagem.
    try:
        # Encontra a posição do último byte 0x00
        padding_start = padded_message.rindex(b"\x00") + 1

        # Retorna a mensagem sem o preenchimento
        return padded_message[padding_start:]
    except ValueError:
        # Se o byte 0x00 não for encontrado, retorna a mensagem original
        return padded_message


def cifrar(msg, public_key):
    # Cifra a mensagem usando a chave pública RSA.
    n, e = public_key
    padded_message = pad_message(msg, n.bit_length() // 8)
    m = int.from_bytes(padded_message, "big")
    c = pow(m, e, n)
    return c.to_bytes((c.bit_length() + 7) // 8, "big")


def decifrar(msg, private_key):
    # Decifra o texto cifrado usando a chave privada RSA.
    n, d = private_key
    c = int.from_bytes(msg, "big")
    m = pow(c, d, n)
    padded_message = m.to_bytes((m.bit_length() + 7) // 8, "big")
    return unpad_message(padded_message)


def assinar_mensagem(mensagem, chave_privada):
    # Calcula o hash da mensagem usando SHA-3 (SHA3-256)
    hash_mensagem = hashlib.sha3_256(mensagem).digest()

    # Desempacota a chave privada
    n, d = chave_privada

    # Converte o hash da mensagem para um número inteiro
    hash_numero = int.from_bytes(hash_mensagem, 'big')

    # Calcula a assinatura usando a chave privada
    assinatura_numero = pow(hash_numero, d, n)

    # Retorna a assinatura como bytes
    return assinatura_numero.to_bytes((n.bit_length() + 7) // 8, 'big')


def verificar_assinatura(mensagem_original, assinatura, chave_publica):
    # Calcula o hash da mensagem original usando SHA-3 (SHA3-256)
    hash_mensagem = hashlib.sha3_256(mensagem_original).digest()

    # Desempacota a chave pública
    n, e = chave_publica

    # Converte a assinatura de bytes para um número inteiro
    assinatura_numero = int.from_bytes(assinatura, 'big')

    # Calcula o valor esperado da assinatura usando a chave pública
    valor_esperado = pow(assinatura_numero, e, n)

    # Compara o valor esperado com o hash da mensagem
    return valor_esperado.to_bytes((n.bit_length() + 7) // 8, 'big') == hash_mensagem


def main():
    while True:
        opcao = input('Modo de execucao\n'
                      '1 - Gerar Chave (Miller-Rabin) \n'
                      '2 - Cifrar RSA \n'
                      '3 - Decifrar RSA \n'
                      '4 - Assinar mensagem \n'
                      '5 - Verificar Assinatura \n'
                      'Opcao: ')

        if opcao not in ['1', '2', '3', '4', '5']:
            print('Opcao invalida.')
            continue

        if opcao == '1':  # Gerar Chave
            chaves = gerar_chave_rsa(1024)
            print('Chave Publica => ', chaves[0])
            print('Chave Privada => ', chaves[1])

        elif opcao == '2':  # Cifrar
            msg = input("Digite a mensagem a ser criptografada: ").encode('utf-8')

            # Obtendo a chave pública do usuário
            chave_publica_input = (input("Digite a chave pública RSA (n, e): ").strip()
                                   .replace('(', '')
                                   .replace(')', '')
                                   .split(','))
            n, e = map(int, chave_publica_input)
            chave_publica = (n, e)

            # Cifrando a mensagem
            cripto = base64.b64encode(cifrar(msg, chave_publica))

            # Exibindo o resultado
            print("Mensagem cifrada (em base64) => ", cripto.decode())

        elif opcao == '3':  # Decifrar
            msg = input("Digite a mensagem a ser decriptografada: ").encode('utf-8')

            # Obtendo a chave pública do usuário
            chave_privada_input = (input("Digite a chave privada RSA (n, d): ").strip()
                                   .replace('(', '')
                                   .replace(')', '')
                                   .split(','))
            n, d = map(int, chave_privada_input)
            chave_privada = (n, d)

            # Cifrando a mensagem
            decripto = decifrar(base64.b64decode(msg), chave_privada)

            # Exibindo o resultado
            print("Mensagem decifrada (em base64) => ", decripto.decode())

        elif opcao == '4':
            # Obtendo a mensagem a ser assinada do usuário
            msg = input("Digite a mensagem a ser assinada: ").encode('utf-8')

            # Obtendo a chave privada do usuário
            chave_privada_input = (input("Digite a chave privada RSA (n, d): ").strip()
                                   .replace('(', '')
                                   .replace(')', '')
                                   .split(','))
            n, d = map(int, chave_privada_input)
            chave_privada = (n, d)

            # Assinando a mensagem
            assinatura = assinar_mensagem(msg, chave_privada)

            # Exibindo a mensagem e a assinatura
            print("Mensagem:", msg.decode())
            print("Assinatura:", base64.b64encode(assinatura).decode())

        elif opcao == '5':
            # Obtendo a mensagem original do usuário
            msg = input("Digite a mensagem original: ").encode('utf-8')

            # Obtendo a chave pública do usuário
            chave_publica_input = (input("Digite a chave pública RSA (n, e): ").strip()
                                   .replace('(', '')
                                   .replace(')', '')
                                   .split(','))
            n, e = map(int, chave_publica_input)
            chave_publica = (n, e)

            # Obtendo e decodificando a assinatura do usuário
            assinatura_base64 = input("Assinatura a verificar (BASE64): ")
            assinatura = base64.b64decode(assinatura_base64)

            # Verificando a assinatura
            verificacao = verificar_assinatura(msg, assinatura, chave_publica)

            print(verificacao)
            # Exibindo o resultado
            if verificacao:
                print("A assinatura é válida.")
            else:
                print("A assinatura é inválida.")

        print('Finalizado!')
        break


if __name__ == '__main__':
    main()
