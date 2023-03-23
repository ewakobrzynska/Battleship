from random import randint
import random

#ROZGRYWKA
row_size = 10  #liczba wierszy
col_size = 10  #liczba kolumn
num_turns = 100 #liczba tur
board = [[0] * col_size for x in range(row_size)] #ustawienie pola gry "pod maska"
board_display = [["O"] * col_size for x in range(row_size)] #pole gry
statki = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
ship_list = [] #lista statkow

#klasa Statek
class Ship:
    def __init__(self,size,orientation,location):
        self.size=size
        #nadanie orientacji statkowi
        if orientation=='poziom' or orientation=='pion':
            self.orientation=orientation
        else:
            raise ValueError("Orientacja musi być pozioma/pionowa")
        #orientacja pozioma - wiersze
        if orientation=='poziom':
            if location['row'] in range(row_size):
                self.coordinates=[]
                for index in range(size):
                    if location['col'] + index in range(col_size):
                        self.coordinates.append({'row': location['row'], 'col': location['col'] + index})
                    else:
                        raise IndexError("Kolumna poza planszą")
            else:
                raise IndexError("Wiersz poza planszą")
        #orientacja pionowa - kolumny
        elif orientation == 'pion':
            if location['col'] in range(col_size):
                self.coordinates=[]
                for index in range(size):
                    if location['row'] + index in range(row_size):
                        self.coordinates.append({'row': location['row'] + index, 'col': location['col']})
                    else:
                        raise IndexError("Wiersz poza planszą")
            else:
                raise IndexError("Kolumna poza planszą")
        #warunek - jesli na kratce znajduje sie juz statek
        if self.filled():
            print_board(board)
            print(" ".join(str(coords) for coords in self.coordinates))
            raise IndexError("Inny statek zajmuje tą pozycje")
        else:
            self.fillBoard()

    #wypełnienie pola gry
    def fillBoard(self):
        for coords in self.coordinates:
            board[coords['row']][coords['col']] = 1
    #sprawdzenie czy na zadanych koordynatach nie znajduje się już statek
    def filled(self):
        for coords in self.coordinates:
            if board[coords['row']][coords['col']]==1:
                return True
        return False
    #do rozgrywki: sprawdzenie czy koordynaty zawierają statek(lub jego czesc)
    def contains(self, location):
        for coords in self.coordinates:
            if coords == location:
                return True
        return False
    #do rozgrywki: funkcja do trafiania w statek
    def destroyed(self):
        for coords in self.coordinates:
            if board_display[coords['row']][coords['col']]=='O':
                return False
            #komorka sprawdzona, ale nie zawiera statku
            elif board_display[coords['row']][coords['col']] == '*':
                raise RuntimeError("Board display inaccurate")
        print("Zatopiony")
        return True

#WYŚWIETLENIE POLA GRY
def print_board(board_array):
    print('   '+'1 '+'2 '+'3 '+'4 '+'5 '+'6 '+'7 '+'8 '+'9 '+'10')
    for r in range(row_size):
        print('{:>2}'.format(str(r + 1))+" "+" ".join(str(c) for c in board_array[r]))
    print()

#WYSZUKIWANIE MOŻLIWEGO ROZMIESZCZENIA STATKU
def search_locations(size, orientation):
  locations = []

  if orientation!='poziom' and orientation!='pion':
    raise ValueError("Orientacja musi być pozioma/pionowa")
  if orientation=='poziom':
    for wiersz in range(10):
        for kolumna in range(10-size+1): #ilość kolumn-rozmiar statku+1(indeks 0)
          if 1 not in board[wiersz][kolumna:kolumna+size]:
#sprawdzenie środka planszy
              if wiersz!=0 and wiersz!=9 and kolumna!=0 and kolumna!=9 and kolumna+size+1!=10:
                if 1 not in board[wiersz+1][kolumna:kolumna+size] and 1 not in board[wiersz-1][kolumna:kolumna+size]:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie pierwszego wiersza
              elif wiersz==0 and kolumna!=0 and kolumna!=9 and kolumna+size+1!=10:
                if 1 not in board[wiersz + 1][kolumna-1:kolumna+size+1] and board[wiersz][kolumna-1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
              elif wiersz==0 and kolumna+size==9:
                if 1 not in board[wiersz + 1][kolumna-1:kolumna+size] and board[wiersz][kolumna-1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie ostatniego wiersza
              elif wiersz==10 and kolumna!=0 and kolumna!=9:
                if 1 not in board[wiersz - 1][kolumna-1:kolumna+size+1] and board[wiersz][kolumna-1]!=1 and board[wiersz][kolumna+size+1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie lewego górnego rogu
              elif wiersz==0 and kolumna==0:
                if 1 not in board[wiersz + 1][kolumna:kolumna+size+1] and board[wiersz][kolumna+size+1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie prawego górnego rogu
              elif wiersz == 0 and kolumna == 9:
                if board[wiersz][kolumna-1]!=1 and 1 not in board[wiersz+1][kolumna-1:kolumna]:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie lewego dolnego rogu
              elif wiersz==9 and kolumna==0:
                if 1 not in board[wiersz -1][kolumna:kolumna + size+1] and board[wiersz][kolumna+1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
#sprawdzenie prawego dolnego rogu
              elif wiersz==9 and (kolumna==9 or kolumna+size==9):
                if 1 not in board[wiersz -1][kolumna:kolumna + size-1] and board[wiersz][kolumna-1]!=1:
                  locations.append({'row': wiersz, 'col': kolumna})
  elif orientation=='pion':
    for kolumna in range(10):
        for wiersz in range(10-size+1): #ilość wierszy-rozmiar statku+1(indeks 0)
          if 1 not in [board[i][kolumna] for i in range(wiersz, wiersz + size)]:
# sprawdzenie środka planszy
              if wiersz != 0 and wiersz != 9 and kolumna != 0 and kolumna != 9 and kolumna + size + 1 != 10:
                  if 1 not in board[wiersz + 1][kolumna:kolumna + size] and 1 not in board[wiersz - 1][kolumna:kolumna + size]:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie pierwszej kolumny
              elif kolumna == 0 and wiersz != 0 and wiersz != 9 and wiersz + size != 9:
                  if 1 not in [board[i][kolumna+1] for i in range(wiersz-1, wiersz + size+1)] and board[wiersz-1][kolumna] != 1 and board[wiersz+1+size][kolumna] != 1:
                    locations.append({'row': wiersz, 'col': kolumna})
              elif kolumna == 0 and wiersz + size == 9:
                  if 1 not in [board[i][kolumna+1] for i in range(wiersz-1, wiersz + size)] and board[wiersz-1][kolumna] != 1:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie ostatniej kolumny
              elif kolumna == 10 and wiersz != 0 and wiersz != 9:
                  if 1 not in [board[i][kolumna-1] for i in range(wiersz-1, wiersz + size+1)] and board[wiersz][kolumna - 1] != 1 and board[wiersz+1+size][kolumna] != 1:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie lewego górnego rogu
              elif wiersz == 0 and kolumna == 0:
                  if 1 not in [board[i][kolumna+1] for i in range(wiersz, wiersz + size+1)] and board[wiersz+size+1][kolumna] != 1:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie prawego górnego rogu
              elif wiersz == 0 and kolumna == 9:
                  if board[wiersz+1+size][kolumna] != 1 and 1 not in [board[i][kolumna-1] for i in range(wiersz, wiersz + size+1)]:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie lewego dolnego rogu
              elif wiersz == 9 and kolumna == 0:
                  if board[wiersz - 1][kolumna]!=1 and board[wiersz][kolumna + 1] != 1:
                    locations.append({'row': wiersz, 'col': kolumna})
# sprawdzenie prawego dolnego rogu
              elif wiersz == 9 and (kolumna == 9 or kolumna + size == 9):
                  if 1 not in [board[i][kolumna-1] for i in range(wiersz-1, wiersz + size)]:
                    locations.append({'row': wiersz, 'col': kolumna})
  return locations

#GENEROWANIE LOSOWEGO USTAWIENIA STATKÓW
def random_location():
    statek_id = random.randint(0, len(statki) - 1)
    size = statki[statek_id]
    statki.pop(statek_id)
    orientation = 'poziom' if randint(0, 1) == 0 else 'pion'
    locations = search_locations(size, orientation)
    if locations == 'None':
        return 'None'
    else:
        return {'location': locations[randint(0, len(locations) - 1)], 'size': size,
                'orientation': orientation}


#POBIERANIE WIERSZA OD GRACZA
def get_row():
    while True:
        try:
            wierszId = int(input("Wiersz: "))
            if wierszId in range(1, row_size + 1):
                return wierszId - 1
            else:
                print("\nNie ma takiego wiersza")
        except ValueError:
            print("\nWprowadz wiersz")

#POBIERANIE KOLUMNY OD GRACZA
def get_col():
    while True:
        try:
            kolumnaId = int(input("Kolumna: "))
            if kolumnaId in range(1, col_size + 1):
                return kolumnaId - 1
            else:
                print("\nNie ma takiej kolumny")
        except ValueError:
            print("\nWprowadź kolumne")




