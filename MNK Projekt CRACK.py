
import time
import random
import csv

import numpy as np


class Player:

    def __init__(self, name: str, player_number: int):
        self._name: str = name
        self._player_number: int = player_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def player_number(self):
        return self._player_number

    @player_number.setter
    def player_number(self, value):
        self._player_number = value

    def make_move(self, board):
        while True:
            row = int(input(f"{self.name}, enter the row number: "))
            col = int(input(f"{self.name}, enter the column number: "))
            try:
                board.array[row, col]
            except IndexError:
                print("Dieses Feld gibt es nicht")
                continue
            except ValueError:
                print("Geben Sie eine Zahl ein")
                continue
            if board.array[row, col] == 1 or board.array[row, col] == 2:
                print("Dieses Feld ist besetzt , bitte wählen sie ein nicht belegtes Feld")
            else:
                break
        return (row, col)


class Board:

    def __init__(self, m: int, n: int, k: int):
        self._m: int = m
        self._n: int = n
        self._k: int = k
        self._array: np.array = np.zeros((self._m, self._n))
        self.board = [[" " for _ in range(self._m)] for _ in range(self._n)]

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value: int):
        self._m = value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value: int):
        self._n = value

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value: int):
        self._k = value

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, value: np.ndarray):
        self._array = value

    def display(self):
        for row in self.board:
            print("|".join(row))
            print("-" * (2 * self._n - 1))

    def has_won(self, player):
        player_number = player.player_number

        # Überprüft Zeilen
        for row in range(self._m):
            for col in range(self._n - self._k + 1):
                if all(self._array[row, col + i] == player_number for i in range(self._k)):
                    return player_number

        # Überprüft Spalten
        for col in range(self._n):
            for row in range(self._m - self._k + 1):
                if all(self._array[row + i, col] == player_number for i in range(self._k)):
                    return player_number

        # Überprüft Diagonale (links oben nach rechts unten)
        for row in range(self._m - self._k + 1):
            for col in range(self._n - self._k + 1):
                if all(self._array[row + i, col + i] == player_number for i in range(self._k)):
                    return player_number

        # Überprüft Diagonale (rechts oben nach links unten)
        for row in range(self._m - self._k + 1):
            for col in range(self._k - 1, self._n):
                if all(self._array[row + i, col - i] == player_number for i in range(self._k)):
                    return player_number

        # Überprüft Unentschieden
        if np.all(self._array != 0):  # Keine leeren Felder mehr
            return 0

        # Spiel geht weiter
        return None

    def is_full(self):
        if all(self.board[row][col] != " " for row in range(self._m) for col in range(self._n)):
            return "Die sind alle belegt"


class AI_Player(Player):
    def __init__(self, name: str, player_number: int, board: Board):
        self._player_number: int = player_number
        self._name: str = name
        super().__init__(self._name, self._player_number)
        self._board: Board = board
        self._moves: list = []
        self._payoff_array: np.ndarray = np.zeros((self._board.array.shape[0], self._board.array.shape[1]))
        self._first: bool = True
        # self._expected_moves: Queue[Move] = Queue()

    @property
    def board(self) -> Board:
        return self._board

    @board.setter
    def board(self, value: Board) -> None:
        self._board = value

    @property
    def payoff_array(self) -> np.ndarray:
        return self._payoff_array

    @payoff_array.setter
    def payoff_array(self, value: np.ndarray) -> None:
        self._payoff_array = value

    @property
    def moves(self) -> list:
        return self._moves

    @moves.setter
    def moves(self, move: tuple) -> None:
        self._moves = self._moves.append(move)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def player_number(self) -> int:
        return self._player_number

    @player_number.setter
    def player_number(self, value: int):
        self._player_number = value


    def successors(self, move) -> dict[str, list]:
        locations: dict[str, list] = {"next_to": [], "diag": []}
        row, col = move[0], move[1]
        m, n = self._board.m, self._board.n

        # Check orthogonal directions (next_to)
        # Right
        if col + 1 < n and self._board.array[row, col + 1] == 0:
            locations["next_to"].append((row, col + 1))
        # Left
        if col - 1 >= 0 and self._board.array[row, col - 1] == 0:
            locations["next_to"].append((row, col - 1))
        # Down (row increases)
        if row + 1 < m and self._board.array[row + 1, col] == 0:
            locations["next_to"].append((row + 1, col))
        # Up (row decreases)
        if row - 1 >= 0 and self._board.array[row - 1, col] == 0:
            locations["next_to"].append((row - 1, col))

        # Check diagonal directions
        # Up-Left
        if row - 1 >= 0 and col - 1 >= 0 and self._board.array[row - 1, col - 1] == 0:
            locations["diag"].append((row - 1, col - 1))
        # Up-Right
        if row - 1 >= 0 and col + 1 < n and self._board.array[row - 1, col + 1] == 0:
            locations["diag"].append((row - 1, col + 1))
        # Down-Left
        if row + 1 < m and col - 1 >= 0 and self._board.array[row + 1, col - 1] == 0:
            locations["diag"].append((row + 1, col - 1))
        # Down-Right
        if row + 1 < m and col + 1 < n and self._board.array[row + 1, col + 1] == 0:
            locations["diag"].append((row + 1, col + 1))

        return locations

    def calc_payoff(self, board, payoff_array: np.ndarray, moves: tuple or None, initial: bool = False) -> np.ndarray:
        vertical: int = payoff_array.shape[0] - 1
        horizontal: int = payoff_array.shape[1] - 1
        layer: int = 0
        if initial:
            while True:
                for i in range(vertical + 1):
                    if payoff_array[vertical - i, layer] == 0 and payoff_array[vertical - i, layer] == 0:
                        payoff_array[vertical - i, layer] = 1 + layer
                    if payoff_array[vertical - i, horizontal - layer] == 0 and payoff_array[
                        vertical - i, horizontal - layer] == 0:
                        payoff_array[vertical - i, horizontal - layer] = 1 + layer
                for i in range(horizontal + 1):
                    if payoff_array[layer, i] == 0 and payoff_array[layer, i] == 0:
                        payoff_array[layer, i] = 1 + layer
                    if payoff_array[vertical - layer, horizontal - i] == 0 and payoff_array[
                        vertical - layer, horizontal - i] == 0:
                        payoff_array[vertical - layer, horizontal - i] = 1 + layer
                layer += 1
                if layer >= int((vertical + 1) / 2) + (vertical + 1) % 2 or layer >= int((horizontal + 1) / 2) + (
                        horizontal + 1) % 2:
                    return payoff_array
        else:
            for move in moves:
                payoff_array[move[0], move[1]] = 0
                locations = self.successors(move)
                for key, value in locations.items():
                    if key == "next_to":
                        for coordinate in value:
                            if board.array[coordinate[0], coordinate[1]] == 0:
                                payoff_array[coordinate[0], coordinate[1]] += 1.4 * min(
                                    int((coordinate[0] + 1) / 2) + (coordinate[0] + 1) % 2,
                                    int((coordinate[1] + 1) / 2) + (coordinate[1] + 1) % 2)
                    elif key == "diag":
                        for coordinate in value:
                            if board.array[coordinate[0], coordinate[1]] == 0:
                                payoff_array[coordinate[0], coordinate[1]] += 1.6 * min(
                                    int((coordinate[0] + 1) / 2) + (coordinate[0] + 1) % 2,
                                    int((coordinate[1] + 1) / 2) + (coordinate[1] + 1) % 2)
            self._payoff_array = payoff_array
            return payoff_array

    def make_move(self, board: Board):
        if len(self._moves) == 0:
            self._payoff_array = self.calc_payoff(board, self._payoff_array, None, initial=True)
            print("3")
        else:
            self._payoff_array = self.calc_payoff(board, self._payoff_array, self._moves)
            self._moves = []
        max_index = self._payoff_array.argmax()
        max_actual_index = np.unravel_index(max_index, self._payoff_array.shape)
        print(max_actual_index)
        return max_actual_index




class AI_schwach(Player):
    def __init__(self, name: str, player_number: int):
        super().__init__(name, player_number)

    def make_move(self, board: Board):
        board = board

        empty_cells = [(r, c) for r in range(board.m) for c in range(board.n) if board.array[r][c] == ' ']

        return random.choice(empty_cells) if empty_cells else None


class RandomAIPlayer(Player):
    def __init__(self, name: str, player_number: int):
        super().__init__(name, player_number)
        self.name = name
        self.player_number = player_number

    def make_move(self, board: Board):
        empty_cells = np.argwhere(board.array == 0)
        if len(empty_cells) == 0:
            return (0, 0)
        move = empty_cells[np.random.choice(len(empty_cells))]
        print(f"KI {self.name} wählt Zeile {move[0]}, Spalte {move[1]}")
        return int(move[0]), int(move[1])


class MyBot(Player):
    def __init__(self, name: str, player_number: int, board: Board):
        super().__init__(name, player_number)
        self._moves: list = []
        self._payoff_array: np.ndarray = np.zeros((board.m, board.n))
        self._first: bool = True
        # Verwende das übergebene Board, nicht ein eigenes
        self._board = board

    @property
    def board(self) -> Board:
        return self._board

    @board.setter
    def board(self, value: Board) -> None:
        self._board = value

    @property
    def payoff_array(self) -> np.ndarray:
        return self._payoff_array

    @payoff_array.setter
    def payoff_array(self, value: np.ndarray) -> None:
        self._payoff_array = value

    @property
    def moves(self) -> list:
        return self._moves

    @moves.setter
    def moves(self, move: tuple) -> None:
        self._moves = self._moves.append(move)

    def successors(self, move) -> dict[str, list]:
        locations: dict[str, list] = {"next_to": [], "diag": []}
        row, col = move[0], move[1]
        m, n = self._board.m, self._board.n

        # Check orthogonal directions (next_to)
        # Right
        if col + 1 < n and self._board.array[row, col + 1] == 0:
            locations["next_to"].append((row, col + 1))
        # Left
        if col - 1 >= 0 and self._board.array[row, col - 1] == 0:
            locations["next_to"].append((row, col - 1))
        # Down (row increases)
        if row + 1 < m and self._board.array[row + 1, col] == 0:
            locations["next_to"].append((row + 1, col))
        # Up (row decreases)
        if row - 1 >= 0 and self._board.array[row - 1, col] == 0:
            locations["next_to"].append((row - 1, col))

        # Check diagonal directions
        # Up-Left
        if row - 1 >= 0 and col - 1 >= 0 and self._board.array[row - 1, col - 1] == 0:
            locations["diag"].append((row - 1, col - 1))
        # Up-Right
        if row - 1 >= 0 and col + 1 < n and self._board.array[row - 1, col + 1] == 0:
            locations["diag"].append((row - 1, col + 1))
        # Down-Left
        if row + 1 < m and col - 1 >= 0 and self._board.array[row + 1, col - 1] == 0:
            locations["diag"].append((row + 1, col - 1))
        # Down-Right
        if row + 1 < m and col + 1 < n and self._board.array[row + 1, col + 1] == 0:
            locations["diag"].append((row + 1, col + 1))

        return locations

    def count_connected(self) -> list[tuple[int, int]]:
        connected = set()  # Verwende ein Set, um doppelte Einträge zu vermeiden

        # Überprüfen der Zeilen
        for row in range(self._board.m):
            for col in range(self._board.n - self._board.k + 1):
                count = sum(self._board.array[row, col + i] == self._player_number for i in range(self._board.k))
                if count >= self._board.k - 2:
                    for i in range(self._board.k):
                        if self._board.array[row, col + i] == 0:
                            connected.add((row, col + i))

        # Überprüfen der Spalten
        for col in range(self._board.n):
            for row in range(self._board.m - self._board.k + 1):
                count = sum(self._board.array[row + i, col] == self._player_number for i in range(self._board.k))
                if count >= self._board.k - 2:
                    for i in range(self._board.k):
                        if self._board.array[row + i, col] == 0:
                            connected.add((row + i, col))

        # Überprüfen der Diagonalen (links oben nach rechts unten)
        for row in range(self._board.m - self._board.k + 1):
            for col in range(self._board.n - self._board.k + 1):
                count = sum(self._board.array[row + i, col + i] == self._player_number for i in range(self._board.k))
                if count >= self._board.k - 2:
                    for i in range(self._board.k):
                        if self._board.array[row + i, col + i] == 0:
                            connected.add((row + i, col + i))

        # Überprüfen der Diagonalen (rechts oben nach links unten)
        for row in range(self._board.m - self._board.k + 1):
            for col in range(self._board.k - 1, self._board.n):
                count = sum(self._board.array[row + i, col - i] == self._player_number for i in range(self._board.k))
                if count >= self._board.k - 2:
                    for i in range(self._board.k):
                        if self._board.array[row + i, col - i] == 0:
                            connected.add((row + i, col - i))

        return list(connected)  # Set zurück in eine Liste umwandeln

    def calc_payoff(self, board, payoff_array: np.ndarray, moves: tuple or None, initial: bool = False) -> np.ndarray:
        vertical: int = payoff_array.shape[0] - 1
        horizontal: int = payoff_array.shape[1] - 1
        layer: int = 0
        if initial:
            while True:
                for i in range(vertical + 1):
                    if payoff_array[vertical - i, layer] == 0 and payoff_array[vertical - i, layer] == 0:
                        payoff_array[vertical - i, layer] = 1 + layer
                    if payoff_array[vertical - i, horizontal - layer] == 0 and payoff_array[
                        vertical - i, horizontal - layer] == 0:
                        payoff_array[vertical - i, horizontal - layer] = 1 + layer
                for i in range(horizontal + 1):
                    if payoff_array[layer, i] == 0 and payoff_array[layer, i] == 0:
                        payoff_array[layer, i] = 1 + layer
                    if payoff_array[vertical - layer, horizontal - i] == 0 and payoff_array[
                        vertical - layer, horizontal - i] == 0:
                        payoff_array[vertical - layer, horizontal - i] = 1 + layer
                layer += 1
                if layer >= int((vertical + 1) / 2) + (vertical + 1) % 2 or layer >= int((horizontal + 1) / 2) + (
                        horizontal + 1) % 2:
                    return payoff_array
        else:
            for move in moves:
                payoff_array[move[0], move[1]] = 0
                locations = self.successors(move)
                for key, value in locations.items():
                    if key == "next_to":
                        for coordinate in value:
                            if board.array[coordinate[0], coordinate[1]] == 0:
                                payoff_array[coordinate[0], coordinate[1]] += 1.4 * min(
                                    int((coordinate[0] + 1) / 2) + (coordinate[0] + 1) % 2,
                                    int((coordinate[1] + 1) / 2) + (coordinate[1] + 1) % 2)
                    elif key == "diag":
                        for coordinate in value:
                            if board.array[coordinate[0], coordinate[1]] == 0:
                                payoff_array[coordinate[0], coordinate[1]] += 1.6 * min(
                                    int((coordinate[0] + 1) / 2) + (coordinate[0] + 1) % 2,
                                    int((coordinate[1] + 1) / 2) + (coordinate[1] + 1) % 2)
            connected = self.count_connected()
            for position in connected:
                payoff_array[position[0], position[1]] += 10 * 10
            self._payoff_array = payoff_array
            return payoff_array

    def make_move(self, board: Board):
        if len(self._moves) == 0:
            self._payoff_array = self.calc_payoff(board, self._payoff_array, None, initial=True)
        else:
            self._payoff_array = self.calc_payoff(board, self._payoff_array, self._moves)
            self._moves = []
        max_index = self._payoff_array.argmax()
        max_actual_index = np.unravel_index(max_index, self._payoff_array.shape)
        print(max_actual_index)
        return max_actual_index


class Game:
    def __init__(self, m: int = 5, n: int = 5, k: int = 4):
        self.running = True
        self._m: int = m
        self._n: int = n
        self._k: int = k
        self._board: Board = Board(self._m, self._n, self._k)
        self._player1: Player = Player(name="1", player_number=1)
        self._player2: Player = Player(name="2", player_number=2)
        self._player3: Player = RandomAIPlayer(name="KI", player_number=3)
        self._player4: MyBot = MyBot(name="stark", player_number=4, board=self._board)
        self._player5: AI_Player = AI_Player(name='schwach', player_number=5, board=self._board)
        
  
    def player_by_modi(self, modi):
        player_by_modi: dict = {
            0: self._player1,
            1: self._player2,
            2: self._player3,
            3: self._player4,
            4: self._player5
        }
        return player_by_modi[modi]
    
    def player_number_by_modi(self, modi) -> int:
        return self.player_by_modi(modi).player_number
    
    def move_by_modi(self, modi) -> tuple[int, int]:
        return self.player_by_modi(modi).make_move(self._board)
    


    def start(self) -> None:
        print('MNK Spiel wird gestartet')

        print(
            'Dieses Spiel heisst MNK.\nEin Spiel bei dem in einem Feld, welches M Anzahl Zeilen und N Anzahl Spalten besteht,\nK Anzahl an Markierungen gesetzt werden soll, welche nebeneinander stehen muessen, um zu gewinnen. ')
        print(f'Die Default-Werte sind: M = {self._m}, N = {self._n}, K = {self._k}.\nMöchten Sie diese ändern?')
        decision: str = input('Eingabe y/n für Entscheidung:')
        if decision == 'y':
            while True:
                try:
                    self._m = int(input('Welcher int Wert soll M haben?: '))
                    self._n = int(input('Welcher int Wert soll N haben?: '))
                    self._k = int(input('Welcher int Wert soll K haben?: '))
                    break
                except ValueError:
                    print('Die Eingabe muss eine ganze Zahl sein! Versuchen Sie es erneut.')
        self._board.display()
        print('Die zwei Spieler setzen abwechselnd Markierungen.')
        print('Um eine Markierung zu setzen, werden die jeweiligen Indizes im Feld benötigt.')
      
        time.sleep(2)
        print(
            'Modi bitte wählen: (0,1) fuer PvP\n, (2,1) fuer zuffals bot vs Palyer\n, (4,1) fuer schwachen bot vs Player \n (3,1) fuer starken bot ... um fuer Bot vs bot tuple mit bot indexie eingeben (reihenfolge der eingabe reflektiert reihenfolge der zuege)')
        modi = input()
        self._modi = tuple(map(int, modi.split(",")))
        print(self._modi[0])
        if self._modi[0] == 0:
            self._player1.name = input('Name des Players 1 eingeben:')
        if self._modi[1] == 1:
            self._player2.name = input('Name des Players 2 eingeben:')
        if self._modi[0] != 4:
            self._player5.opponent = self.player_by_modi(self._modi[0])
        if self._modi[1] != 4:
            self._player5.opponent = self.player_by_modi(self._modi[1])
        self._player1.player_number = 1
        self._player2.player_number = 2
        print(self._board.array)
        self._player1.player_number = 1
        self._player2.player_number = 2
       

    def game_loop(self) -> None:
        move_player1: tuple[int, int]
        move_player2: tuple[int, int]
        gewonnen: int

        while self.running:
            
            move_player1 = self.move_by_modi(self._modi[0])
            self._player4.moves.append((move_player1[0], move_player1[1]))
            self._player5.moves.append((move_player1[0], move_player1[1]))
            print(move_player1)
            print(self._board.array)
            self._board.array[
                move_player1[0] + 0, move_player1[1]] = self.player_number_by_modi(self._modi[0])
            
            print(self._board.array)
            gewonnen = self._board.has_won(self.player_by_modi(self._modi[0]))
            if gewonnen == self.player_number_by_modi(self._modi[0]):
                print(f'Hurra...{self.player_by_modi(self._modi[0]).name} hat gewonnen Herzlichen Glückwunsch! Nächstes Mal PLayer 2')
                return self.player_by_modi(self._modi[0]).name
            elif gewonnen == 0:
                print('Ein Unentschieden, da alle Felder belegt sind')
                break

            move_player2 = self.move_by_modi(self._modi[1])
            self._player4.moves.append((move_player2[0], move_player2[1]))
            self._player5.moves.append((move_player2[0], move_player2[1]))
            self._board.array[
                move_player2[0] + 0, move_player2[1] ] = self.player_number_by_modi(self._modi[1])
            
            print(self._board.array)
            gewonnen = self._board.has_won(self.player_by_modi(self._modi[1]))
            if gewonnen == self.player_number_by_modi(self._modi[1]):
                print(f'Hurra...{self.player_by_modi(self._modi[1]).name} hat gewonnen Herzlichen Glückwunsch! Nächstes Mal Player 1')
                return self.player_by_modi(self._modi[1]).name
            elif gewonnen == 0:
                print('Ein Unentschieden, da alle Felder belegt sind')
                break



if __name__ == '__main__':
    game: Game = Game()
    game.start()
    game.game_loop()
