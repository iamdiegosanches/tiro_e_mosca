import random

num_comp = str(random.randint(100, 1000))
print(num_comp)
rodando = True

historico_palpites = []
print("JOGO DO TIRO E MOSCA - digite 0 para sair")
while rodando:
    palpite = str(input("Digite o texto a ser enviado ao servidor:\n"))
    if palpite == '0':
        rodando = False
        continue
    if len(palpite) != 3 or not palpite.isdigit():
        print("O palpite deve conter 3 números")
        continue

    tiro = 0
    mosca = 0

    num_comp_copy = list(num_comp)
    palpite_copy = list(palpite)

    for i in range(3):
        if palpite_copy[i] == num_comp_copy[i]:
            tiro += 1
            num_comp_copy[i] = "x"
            palpite_copy[i] = "y"

    for i in range(3):
        if palpite_copy[i] in num_comp_copy:
            mosca += 1
            index = num_comp_copy.index(palpite_copy[i])
            num_comp_copy[index] = "x"

    historico_palpites.append(f'{palpite} - {tiro}t{mosca}m')
    print(f'{palpite} - {tiro}t{mosca}m')
    if tiro == 3:
        break

print("FIM DE JOGO!!!!!!!")
