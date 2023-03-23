from random import randint

#KLASA DO PRZECHOWYWANIA WSPÓŁRZĘDNYCH (X,Y)
class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

#OBSŁUGA WYJĄTKÓW
class OutOfBoardException(Exception):
    def __str__(self):
        return "Próbujesz strzelać poza plansze!"


class BoardUsedException(Exception):
    def __str__(self):
        return "Już zastrzeliłeś tą kratkę"

class BoardWrongShipException(Exception):
    pass

#KLASA STATEK
class Ship:
    def __init__(self, kratka, maszty, orientacja):
        self.kratka = kratka
        self.maszty = maszty
        self.orientacja = orientacja
        self.doOdstrzalu = maszty

#FUNCKJA ZWRACAJĄCA KRATKI STATKU
    @property
    def statekPlynie(self):
        wspolStatku = [] #lista wspolrzednych statku
        for i in range(self.maszty):
            wspolX = self.kratka.x
            wspolY = self.kratka.y
            if self.orientacja == 0: #ustawienie statku zorientowanego poziomo
                wspolX += i
            elif self.orientacja == 1: #ustawienie statku zorientowanego pionowo
                wspolY += i
            wspolStatku.append(Coords(wspolX, wspolY))
        return wspolStatku

'''----------KLASA POLA DO GRY-----------'''
class Board:
#DEKLARACJA ROZGRYWKI
    def __init__(self, hid=False, size=10):
        self.size = size #rozmiar
        self.hid = hid #plansza ze statkami ukryta przed graczem
        self.count = 0 #licznik zatopionych statków
        self.pole = [[" "] * size for _ in range(size)] #wypełnienie pola gry
        self.busy = [] #zajęte kratki
        self.ships = [] #lista statków

#FUNKCJA DODAJĄCA STATEK
    def add_ship(self, ship):
        for d in ship.statekPlynie:
            if self.out(d) or d in self.busy: #warunek: statek poza polem gry lub statek na zajętym polu
                raise BoardWrongShipException()
        for d in ship.statekPlynie:
            self.pole[d.x][d.y] = "■" #oznaczenie statku na kratce
            self.busy.append(d) #oznaczenie kratki d jako zajętej

        self.ships.append(ship) #dodanie utworzonego statku do listy statków
        self.contour(ship) #obrysowanie pól graniczących ze statkiem

#FUNKCJA NIEPOZWALAJĄCA NA STYKANIE SIĘ STATKÓW BOKAMI I ROGAMI
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.statekPlynie:
            for dx, dy in near:
                cur = Coords(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    self.busy.append(cur)

#FUNCKCJA WYŚWIETLENIA POLA GRY
    def __str__(self):
        wiersz = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|"
        for i, row in enumerate(self.pole):
            wiersz += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid: #plansza dla gracza
            wiersz = wiersz.replace("■", " ") #zamiana pola oznaczonego statkiem jako pole niewiadome dla użytkownika
        return wiersz

#FUNKCJA SPRAWDZAJĄCA CZY STATEK NIE BĘDZIE ZNAJDOWAŁ SIĘ POZA POLEM GRY
    def out(self, kratka):
        return not ((0 <= kratka.x < self.size) and (0 <= kratka.y < self.size))

#FUNKCJA DO STRZELANIA W STATEK
    def strzel(self, kratka):
        if self.out(kratka):
            raise OutOfBoardException()
        if kratka in self.busy:
            raise BoardUsedException()

        self.busy.append(kratka)
        for ship in self.ships:
            if kratka in ship.statekPlynie: #jesli na kratce znajduje sie maszt statku
                ship.doOdstrzalu -= 1 #-1 maszt statku
                self.pole[kratka.x][kratka.y] = "X" #oznacz kratke jako trafione
                if ship.doOdstrzalu == 0: #jesli maszt=0 => zniszczono caly statek
                    self.count += 1 #licznik zniszczonych statkow +1
                    self.contour(ship, verb=True)
                    print("Statek jest zniszczony!")
                    return False
                else:
                    print("Statek został trafiony!")
                    return True

        self.pole[kratka.x][kratka.y] = "*" #kratka sprawdzona, ale nietrafiona
        print("Pudło!")
        return False

    def begin(self):
        self.busy = []

'''------------KLASA GRACZA------------'''
class Player:
    def __init__(self, board):
        self.board = board
#FUNKCJA DO WPROWADZENIA WSPOLRZEDNYCH PRZEZ GRACZA
    def wprowadzWspolrzedne(self):
        while True:
            cords = input("Twój ruch: ").split() #pobranie wspolrzednych z klawiatury
            if len(cords) != 2: #jesli gracz podal niepoprawna ilosc argumentow
                print("Musisz podac 2 wspolrzedne!")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()): #jesli gracz podal niepoprawne dane
                print("Wspolrzedne musza byc dodatnimi liczbami calkowitymi!")
                continue
            return Coords(int(x) - 1, int(y) - 1) #zwrocenie formatu odpowiedniego dla tablic

    def wykonajRuch(self):
        while True:
            cel = self.wprowadzWspolrzedne()
            strzal = self.board.strzel(cel)
            return strzal


'''--------------KLASA ROZGRYWKI--------------'''
class Game:
    def __init__(self, size=10):
        self.size = size
        plansza = self.rozmiescStatki()
        plansza.hid=True
        self.player = Player(plansza)
#FUNKCJA GENERUJĄCA LOSOWE ROZMIESZCZENIE STATKÓW NA POLU GRY
    def rozmiescStatki(self):
        statki = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        for statek in statki:
            while True:
                ship = Ship(Coords(randint(0, self.size), randint(0, self.size)), statek, randint(0, 1)) #generowanie statku
                try:
                    board.add_ship(ship) #dodanie wygenerowanego statku na plansze
                    break
                except:
                    pass
        board.begin()
        return board
#FUNKCJA ODPOWIADAJĄCA NA OBSŁUGĘ ROZGRYWKI
    def start(self):
        for ruch in range(30):
            print("-" * 20)
            print(self.player.board)
            self.player.wykonajRuch()
            if self.player.board.count == 10: #wygrana w grze (liczba zastrzelonych statkow=0)
                print("***Wygrałeś!***")
                return True
        print("Niestety przegrałeś")
#URUCHOMIENIE GRY
Game().start()