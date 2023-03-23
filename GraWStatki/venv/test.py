from random import randint as rand
from time import sleep
import numpy as np
import scipy
from scipy.spatial import distance


# Klasa obslugujaca plansze do gry
class Board:

    def __init__(self):
        self.__playerBoard = [['O'] * 10 for _ in range(10)]
        self.__computerBoard = [['O'] * 10 for _ in range(10)]

    # Funkcja rysujaca plansze
    def printBoard(self, pH=None, cH=None):
        label = "ABCDEFGHIJ"
        colors = dict(L='\033[41m',
                      S='\033[42m',
                      N='\033[43m',
                      F='\033[45m',
                      P='\033[46m',
                      T='\033[47m',
                      Z='\033[100m',
                      K='\033[105m')
        fgBlack = '\033[30m'
        reset = '\033[0m'

        self.clear_screen()
        print("             \033[04mP L A Y E R B O A R D\033[0m"
              "                                 \033[04mC O M P U T E R B O A R D\033[0m")
        print()

        for i in range(10):
            if i != 0:
                print("  " + str(i + 1), end=' ')
            else:
                print("     " + str(i + 1), end=' ')
        print("           ", end="")
        for i in range(10):
            if i != 0:
                print("  " + str(i + 1), end=' ')
            else:
                print("     " + str(i + 1), end=' ')
        print()
        print("   -----------------------------------------              -----------------------------------------")

        for i in range(10):

            print(" " + label[i], end=' |')
            for j in range(10):
                if self.__playerBoard[i][j] == 'X':
                    print(colors[self.findPoint(i, j, pH)] + fgBlack + " X " + reset, end="|")
                elif self.__playerBoard[i][j] == 'O':
                    print("   ", end="|")
                elif self.__playerBoard[i][j] == '*':
                    print(" * ", end="|")
                else:
                    print(colors[self.__playerBoard[i][j]] + fgBlack + " " + self.__playerBoard[i][j] + " " + reset,
                          end="|")

            print("           ", end="")

            print(" " + label[i], end=' |')
            for j in range(10):
                if self.__computerBoard[i][j] == 'X':
                    print(colors[self.findPoint(i, j, cH)] + fgBlack + " X " + reset, end="|")
                elif self.__computerBoard[i][j] == '*':
                    print(" * ", end="|")
                else:
                    print("   ", end="|")

            print()
            print("   -----------------------------------------              -----------------------------------------")

    # Funkcja szukajaca kolor statku do wypisania
    def findPoint(self, x, y, hitted):
        for hit in hitted.keys():
            for point in hitted[hit]:
                if point[0] == x and point[1] == y:
                    return hit

    # Funkcja czyszczaca okno konsoli
    def clear_screen(self):
        print('\033[2J\033[0;0H')

    @property
    def playerBoard(self):
        return self.__playerBoard

    @property
    def computerBoard(self):
        return self.__computerBoard

    @playerBoard.setter
    def playerBoard(self, board):
        self.__playerBoard = board

    @computerBoard.setter
    def computerBoard(self, board):
        self.__computerBoard = board


# Klasa zawierajaca implementacje rozgrywki
class GameLogic:
    def __init__(self):
        self.ships = {
            "L": (4, 'Lotniskowiec'),
            "S": (3, 'Szturmowiec'),
            "N": (3, 'Niszczyciel'),
            "F": (2, 'Fregata'),
            "P": (2, 'Pancernik'),
            "K": (1, 'Kuter'),
            "Z": (1, 'Zbiornikowiec'),
            "T": (1, 'Tralowiec'),
        }

        self.__isHitted = False
        self.__toShoot = {}
        self.__playerHitted = dict(L=[], S=[], N=[], F=[], P=[], T=[], Z=[], K=[])
        self.__computerHitted = dict(L=[], S=[], N=[], F=[], P=[], T=[], Z=[], K=[])

    # Funkcja dodajaca statki gracza
    def playerShips(self, board):
        for ship in self.ships.keys():
            while True:
                board.printBoard()

                shipInfo = self.ships[ship]
                print(f"\033[93mUstawianie: {shipInfo[1]} {shipInfo[0]} masztowy\033[0m")

                x, y, direction = self.getCords()
                isValid = self.check(x, y, direction, shipInfo[0], board.playerBoard)

                if isValid:
                    self.placeShip(x, y, direction, ship, board.playerBoard)
                    break
                else:
                    print("Nie mozna wstawic statku w podanym miejscu")
                    input("Wcisnij enter")

        board.printBoard()

    # Funkcja dodajaca statki komputera
    def computerShips(self, board):
        for ship in self.ships.keys():
            while True:
                shipInfo = self.ships[ship]

                x, y, direction = self.getCompCords()
                isValid = self.check(x, y, direction, shipInfo[0], board.computerBoard)

                if isValid:
                    self.placeShip(x, y, direction, ship, board.computerBoard)
                    break

        board.printBoard()

    # Funkcja przyjmujaca wspolrzedne i kierunek statku od gracza
    def getCords(self):
        translator = dict(a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8, j=9)
        while True:
            cords = input(
                "Podaj wspolrzedne i ulozenie (pionowo - v, poziomo - h)"
                " statku oddzielone spacjami: ").lower().split(" ")

            try:
                if len(cords) != 3:
                    raise Exception("Niepoprawna ilosc argumentow")

                if cords[0] not in translator:
                    raise Exception("Niepoprawne dane")
                else:
                    cords[0] = translator.get(cords[0])

                if not (cords[2] != "v" or cords[2] != "h"):
                    raise Exception("Niepoprawne dane")

                cords[1] = int(cords[1]) - 1

                if cords[1] < 0 or cords[1] > 9:
                    raise Exception("Niepoprawne dane")

                return cords[0], cords[1], cords[2]
            except ValueError:
                print("Niepoprawne dane")
            except Exception as e:
                print(e)

    # Funkcja losujaca wspolrzedne i kierunek statku dla komputera
    def getCompCords(self):
        cords = [None, None, None]
        cords[0] = rand(0, 9)
        cords[1] = rand(0, 9)
        cords[2] = "v" if rand(0, 1) else "h"

        return cords[0], cords[1], cords[2]

    # Funkcja sprawdzajaca czy statek miesci sie w podanych wspolrzednych
    def check(self, x, y, direction, ship, board):
        if direction == "v":
            if x + ship > 10:
                return False
            else:
                for i in range(ship):
                    if board[x + i][y] != "O":
                        return False
        else:
            if y + ship > 10:
                return False
            else:
                for i in range(ship):
                    if board[x][y + i] != "O":
                        return False
        return True

    # Funkcja ustawiajaca statek na planszy
    def placeShip(self, x, y, direction, ship, board):
        if direction == 'v':
            for i in range(self.ships[ship][0]):
                board[x + i][y] = ship
        else:
            for i in range(self.ships[ship][0]):
                board[x][y + i] = ship

    # Funkcja sprawdzajaca czy nastapila wygrana
    def isWin(self, board):
        for i in range(10):
            for j in range(10):
                if board[i][j] in ["L", "S", "N", "F", "P", "T", "Z", "K"]:
                    return False
        return True

    # Funkcja sprawdzajaca czy statek zostal zatopiony
    def isSunk(self, ship, board, computer=False):
        sunk = True
        for i in range(10):
            for j in range(10):
                if board[i][j] == ship:
                    sunk = False
        if sunk:
            print(f"Zatopiono {self.ships[ship][0]} masztowy {self.ships[ship][1].lower()}")
            if computer and self.ships[ship][0] > 1:
                self.__toShoot.pop(ship)
                sleep(2)

    # Funckja odpowiadajaca za ruch gracza
    def playerMove(self, board):
        while True:
            x, y = self.shootCords()
            shootStatus = self.shoot(x, y, board.computerBoard)

            if shootStatus != "used" and shootStatus != "miss":
                self.__computerHitted[shootStatus].append((x, y))

                board.printBoard(pH=self.__playerHitted, cH=self.__computerHitted)
                print(f"Trafiono {self.ships[shootStatus][0]} masztowy {self.ships[shootStatus][1].lower()}")

                self.isSunk(shootStatus, board.computerBoard)

                if self.isWin(board.computerBoard):
                    return True

                continue
            elif shootStatus == "miss":
                board.printBoard(pH=self.__playerHitted,
                                 cH=self.__computerHitted)
                print("Pudlo")
                break
            elif shootStatus == "used":
                board.printBoard(pH=self.__playerHitted, cH=self.__computerHitted)
                print("Juz trafiano w to miejsce")
                continue

        return False

    # Funckja odpowiadajaca za ruch komputera
    def computerMove(self, board):
        while True:
            x, y = self.shootCompCords()
            shootStatus = self.shoot(x, y, board.playerBoard)

            if shootStatus != "used" and shootStatus != "miss":
                self.__isHitted = True
                self.aim(shootStatus, x, y)

                board.printBoard(pH=self.__playerHitted, cH=self.__computerHitted)
                print(f"Komputer trafil {self.ships[shootStatus][0]} masztowy {self.ships[shootStatus][1].lower()}")

                sleep(2)
                self.isSunk(shootStatus, board.playerBoard, computer=True)

                if self.isWin(board.playerBoard):
                    return True

                continue
            elif shootStatus == "miss":
                board.printBoard(pH=self.__playerHitted, cH=self.__computerHitted)
                print("Komputer spudlowal")
                break
            elif shootStatus == "used":
                board.printBoard(pH=self.__playerHitted, cH=self.__computerHitted)
                continue

        return False

    # Funkcja pobierajace od gracza wspolrzedne kolejnego strzalu
    def shootCords(self):
        translator = dict(a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8, j=9)
        while True:
            cords = input("Podaj wspolrzedne oddzielone spacja: ").lower().split(" ")

            try:
                if len(cords) != 2:
                    raise Exception("Niepoprawna ilosc argumentow")

                if cords[0] not in translator:
                    raise Exception("Niepoprawne dane")
                else:
                    cords[0] = translator.get(cords[0])

                cords[1] = int(cords[1]) - 1

                if cords[1] < 0 or cords[1] > 9:
                    raise Exception("Niepoprawne dane")

                return cords[0], cords[1]
            except ValueError:
                print("Niepoprawne dane")
            except Exception as e:
                print(e)

    # Funkcja losujaca wspolrzedne strzalu dla komputera
    # lub zwracajaca wspolrzedne w poblizu trafionego statku
    def shootCompCords(self):
        if self.__isHitted:
            if len(self.__toShoot) == 0:
                self.__isHitted = False
            else:
                cords = self.__toShoot.get(next(iter(self.__toShoot)))[0]
                self.__toShoot.get(next(iter(self.__toShoot))).remove(cords)
                return cords[0], cords[1]

        cords = [None, None]
        cords[0] = rand(0, 9)
        cords[1] = rand(0, 9)
        return cords[0], cords[1]

    # Funkcja sprawdzajaca czy dla podanych wspolrzednych nastapilo trafienie
    def shoot(self, x, y, board):
        if board[x][y] == "O":
            board[x][y] = "*"
            return "miss"
        elif not (board[x][y] == "O" or board[x][y] == "*" or board[x][y] == "X"):
            ship = board[x][y]
            board[x][y] = "X"
            return ship
        elif board[x][y] == "*" or board[x][y] == "X":
            return "used"

    # Funkcja wyliczajaca mozliwe ruchy dla komputera gdy statek zostal trafiony
    def aim(self, ship, x, y):
        if len(self.__playerHitted[ship]) == 0 and self.ships[ship][0] != 1:
            toShoot = []

            for i in range(1, self.ships[ship][0]):
                if x - i >= 0:
                    toShoot.append((x - i, y))
                if x + i <= 9:
                    toShoot.append((x + i, y))
                if y - i >= 0:
                    toShoot.append((x, y - i))
                if y + i <= 9:
                    toShoot.append((x, y + i))

            self.__toShoot[ship] = toShoot
        elif len(self.__playerHitted[ship]) == 1 and self.ships[ship][0] > 2:
            firstHit = self.__playerHitted[ship][0]
            toShoot = self.__toShoot[ship]

            if firstHit[0] == x:
                for shoot in toShoot:
                    if shoot[0] != x:
                        toShoot.remove(shoot)
            elif firstHit[1] == y:
                for shoot in toShoot:
                    if shoot[1] != y:
                        toShoot.remove(shoot)

            self.__toShoot[ship] = toShoot

        self.__playerHitted[ship].append((x, y))


# Klasa odpowiedzialna za zarzadzanie gra
class Game:
    # Konstruktor
    def __init__(self):
        self.gameBoard = Board()
        self.gameLogic = GameLogic()

    # Funkcja resetujaca stan gry
    def reset(self):
        del self.gameBoard
        del self.gameLogic
        self.gameBoard = Board()
        self.gameLogic = GameLogic()

    # Funkcja zawierajaca menu
    def menu(self):
        self.gameBoard.clear_screen()
        print("\u001B[104m                                   \033[0m\n"

              "\u001B[104m \u001B[107m     \u001B[104m \u001B[107m     \u001B[104m   \u001B[107m  \u001B[104m  "
              "\u001B[107m     \u001B[104m \u001B[107m  \u001B[104m \u001B[107m  \u001B[104m \u001B[107m   \u001B["
              "104m \033[0m\n"

              "\u001B[104m \u001B[107m \u001B[104m     \u001B[107m \u001B[104m \u001B[107m \u001B[104m \u001B[107m "
              "\u001B[104m  \u001B[107m \u001B[104m \u001B[107m \u001B[104m  \u001B[107m \u001B[104m \u001B[107m "
              "\u001B[104m \u001B[107m \u001B[104m  \u001B[107m \u001B[104m \u001B[107m \u001B[104m   \u001B[107m "
              "\u001B[104m  \033[0m\n"

              "\u001B[104m \u001B[107m     \u001B[104m   \u001B[107m \u001B[104m    \u001B[107m \u001B[104m \u001B["
              "107m \u001B[104m    \u001B[107m \u001B[104m    \u001B[107m  \u001B[104m    \u001B[107m \u001B[104m  "
              "\033[0m\n"

              "\u001B[104m     \u001B[107m \u001B[104m   \u001B[107m \u001B[104m    \u001B[107m   \u001B[104m    "
              "\u001B[107m \u001B[104m    \u001B[107m \u001B[104m \u001B[107m \u001B[104m   \u001B[107m \u001B[104m  "
              "\033[0m\n"

              "\u001B[104m \u001B[107m     \u001B[104m  \u001B[107m   \u001B[104m  \u001B[107m  \u001B[104m \u001B["
              "107m  \u001B[104m  \u001B[107m   \u001B[104m  \u001B[107m  \u001B[104m \u001B[107m  \u001B[104m "
              "\u001B[107m   \u001B[104m \033[0m\n"
              "\u001B[104m                                   \033[0m")
        print("\033[0m")

        print("===================================")
        print("=              MENU               =")
        print("===================================\n")
        print("1. Start gry")
        print("2. Instrukcje")
        print("3. Wyjscie z gry\n")
        print("===================================\n")

        while True:
            option = input("Podaj numer opcji do wykonania: ")
            if option == "1":
                self.play()
                break
            elif option == "2":
                self.instructions()
                break
            elif option == "3":
                exit()
            else:
                print("Nie ma takiej opcji!")

    # Funkcja zawierajaca instrukcje gry
    def instructions(self):
        self.gameBoard.clear_screen()
        print("=================================================")
        print("=                  INSTRUKCJE                   =")
        print("=================================================\n")
        print("Gracz posiada dwie plansze o wielkosci 10x10 pol.\n"
              "Pola oznaczone sa poprzez wspolrzedne literami od A do J i liczbami od 1 do 10.\n"
              "Na jednym z kwadratow gracz widzi swoje statki, ktorych polozenie bedzie odgadywal przeciwnik. \n"
              "Na drugim zaznaczone sa trafione statki przeciwnika i oddane strzaly.\n"
              "Statki moga byc ustawiane w pionie i poziomie, moga sie stykac, ale nie moga na siebie nachodzic.\n"
              "Gracz i komputer posiadaja po jednym czteromasztowcu, dwoch trojmasztowcach, dwoch dwumasztowcach i "
              "trzech jednomasztowcach.\n"
              "Po rozpoczeciu gry gracz podaje wspolrzedne rufy statku i kierunek w ktorym ma byc skierowany.\n"
              "Przyklad: c 4 v\n"
              "Po dodaniu wszystkich statkow gracz i komputer naprzemiennie probuja trafic statek przeciwnika.\n"
              "Aby oddac strzal nalezy podac wspolrzedne do ktorych ma zostac oddany.\n"
              "Wygranym zostaje ta strona, ktora pierwsza zatopi wszystkie statki przeciwnika.")
        print("=================================================\n")

        input("Wcisnij dowolny klawisz aby wrocic ")
        self.menu()

    # Funckja odpowiadajaca za rozgrywke
    def play(self):
        self.gameLogic.playerShips(self.gameBoard)
        self.gameLogic.computerShips(self.gameBoard)
        self.gameBoard.printBoard()

        while True:
            if self.gameLogic.playerMove(self.gameBoard):
                print("\u001B[93mGratulacje! Wygrales!\033[0m")
                break
            input("Zakoncz ture")

            if self.gameLogic.computerMove(self.gameBoard):
                print("\u001B[93mPorazka. Komputer wygral.\033[0m")
                break

        input("Wcisnij enter aby kontynuować ")
        self.reset()
        self.menu()


def main():
    game = Game()
    game.menu()


if __name__ == "__main__":
    main()