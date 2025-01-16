from collections import Counter


class TiroMosca:
    def __init__(self, id):
        self.id = id
        self.turn = 0
        self.winner = None
        self.ready = False
        self.secret = [["" for _ in range(3)] for _ in range(2)]
        self.post_secret = False
        self.mosca = 0
        self.tiro = 0
        self.history = [[], []]
        self.quit = [0, 0]

    def set_number(self, player, number, index):
        print(self.secret)
        print(self.secret[player][index] == "") 
        if self.secret[player][index] == "":
            self.secret[player][index] = number
            self.post_secret = all(all(num != "" for num in secret) for secret in self.secret)
            print(self.secret)
            return True
        return False

    def set_numbers(self, player, numbers: list):
        if len(numbers) != 3 or not all(0 <= num <= 9 for num in numbers):
            raise ValueError("Os números devem estar entre 0 e 9 e conter exatamente 3 dígitos.")
        for i, number in enumerate(numbers):
            set_number = self.set_number(player, number, i)
            if not set_number:
                return False
        return True

    def play(self, player, guess: list):
        if not self.ready:
            raise ValueError("Ambos os jogadores precisam definir seus números secretos antes de começar.")
        if self.turn != player:
            raise ValueError("Não é a sua vez de jogar.")
        if len(guess) != 3 or not all(0 <= num <= 9 for num in guess):
            raise ValueError("Os palpites devem conter exatamente 3 números entre 0 e 9.")

        self.mosca = 0
        self.tiro = 0
        opponent = 1 - player

        # Contagem de "Moscas"
        for i in range(3):
            if self.secret[opponent][i] == guess[i]:
                self.mosca += 1

        # Contagem de "Tiros"
        opponent_counts = Counter(self.secret[opponent])
        for num in guess:
            if opponent_counts[num] > 0:
                self.tiro += 1
                opponent_counts[num] -= 1
        self.tiro -= self.mosca  # Remove "Moscas" dos "Tiros"

        # Armazena o palpite no histórico
        self.history[player].append((guess, self.tiro, self.mosca))

        # Troca de turnos
        self.turn = 1 - self.turn

        # Verifica condição de vitória
        if self.mosca == 3:
            self.winner = player

    def connected(self):
        return self.ready

    def reset(self):
        self.turn = 0
        self.winner = None
        self.secret = [["" for _ in range(3)] for _ in range(2)]
        self.mosca = 0
        self.tiro = 0
        self.history = [[], []]
